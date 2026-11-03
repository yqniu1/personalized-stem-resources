# Multilevel foundations refresher: every number quoted in tutorial.md comes from here.
# Run from the repository root:  Rscript modules/multilevel-foundations/multilevel_refresher.R
# Requires lme4. Seeded; output is deterministic for a given R/lme4 version.
suppressPackageStartupMessages(library(lme4))
options(digits = 4, width = 100)
say <- function(...) cat(sprintf(...), "\n", sep = "")
rule <- function(title) cat("\n==== ", title, " ====\n", sep = "")

# --------------------------------------------------------------------------
rule("Part 1. Toy data: 3 schools x 4 students, 0-12 belonging score")
toy <- data.frame(
  school = factor(rep(c("A", "B", "C"), each = 4)),
  y      = c(4, 6, 8, 10,   2, 4, 6, 8,   5, 7, 9, 11),
  program = rep(c(1, 0, 1), each = 4)   # a school-level variable
)
n <- 4; J <- 3; grand <- mean(toy$y)
means <- tapply(toy$y, toy$school, mean)
ssw <- sum((toy$y - means[toy$school])^2)
ssb <- n * sum((means - grand)^2)
msw <- ssw / (J * (n - 1)); msb <- ssb / (J - 1)
say("grand mean = %.4f; school means = %s", grand, paste(means, collapse = ", "))
say("SS_between = %.4f (df %d), SS_within = %.4f (df %d), SS_total = %.4f",
    ssb, J - 1, ssw, J * (n - 1), sum((toy$y - grand)^2))
say("MS_between = %.4f, MS_within = %.4f, F = %.4f, p = %.4f",
    msb, msw, msb / msw, pf(msb / msw, J - 1, J * (n - 1), lower.tail = FALSE))
print(anova(lm(y ~ school, data = toy)))

rule("Part 1b. Variance components from the ANOVA table")
tau2 <- (msb - msw) / n
say("tau^2 (between-school) = (MSB - MSW)/n = %.4f", tau2)
say("sigma^2 (within-school) = MSW = %.4f", msw)
say("ICC = tau^2/(tau^2+sigma^2) = %.4f", tau2 / (tau2 + msw))
say("Variance of observed school means = %.4f = tau^2 + sigma^2/n = %.4f",
    var(means), tau2 + msw / n)
# Snijders & Bosker (2012) sec. 11.3: respondents per unit for target reliability lambda0.
n_min <- function(lambda0, icc) lambda0 * (1 - icc) / ((1 - lambda0) * icc)
say("n_min check against S&B Example 11.2 (lambda0 .80, ICC .40) = %.1f (book: 6)", n_min(.80, .40))
say("respondents per school for school-mean reliability .70 / .80 at ICC .10: %.1f / %.1f",
    n_min(.70, .10), n_min(.80, .10))
say("same at ICC .05: %.1f / %.1f", n_min(.70, .05), n_min(.80, .05))

rule("Part 1c. Same data as a random-intercept model (REML)")
m_re <- lmer(y ~ 1 + (1 | school), data = toy, REML = TRUE)
print(VarCorr(m_re), comp = "Variance")
say("fixed intercept = %.4f", fixef(m_re)[1])
lambda <- tau2 / (tau2 + msw / n)
say("shrinkage factor lambda = tau^2/(tau^2 + sigma^2/n) = %.4f", lambda)
shrunk <- coef(m_re)$school[, 1]
print(data.frame(school = levels(toy$school), raw_mean = as.numeric(means),
                 fixed_effect_estimate = as.numeric(means),
                 random_effect_prediction = round(shrunk, 4),
                 by_formula = round(grand + lambda * (means - grand), 4)))

rule("Part 1d. Fixed effects cannot estimate a school-level predictor")
print(coef(lm(y ~ school + program, data = toy)))
m_re_prog <- suppressMessages(lmer(y ~ program + (1 | school), data = toy))
say("random-intercept model: program coefficient = %.4f", fixef(m_re_prog)["program"])
say("singular fit: %s; remaining school variance = %.4f",
    isSingular(m_re_prog), as.data.frame(VarCorr(m_re_prog))$vcov[1])

# --------------------------------------------------------------------------
rule("Part 2. Simulated school survey: students in schools in districts in states")
set.seed(20261103)
var_true <- c(district = 0.04, school = 0.06, student = 0.90)
state_effect <- c(S1 = 0, S2 = 0.30, S3 = -0.20)           # 3 states: fixed
d <- do.call(rbind, lapply(names(state_effect), function(s) {
  do.call(rbind, lapply(1:12, function(k) {                 # 12 districts per state
    u_d <- rnorm(1, 0, sqrt(var_true["district"]))
    n_sch <- sample(2:6, 1)
    do.call(rbind, lapply(seq_len(n_sch), function(j) {
      u_s <- rnorm(1, 0, sqrt(var_true["school"]))
      n_i <- sample(c(8, 15, 25, 40, 80), 1)               # uneven response counts
      data.frame(state = s, district = paste(s, k, sep = "-"),
                 school = paste(s, k, j, sep = "-"),
                 y = 3.2 + state_effect[s] + u_d + u_s + rnorm(n_i, 0, sqrt(var_true["student"])))
    }))
  }))
}))
d$state <- factor(d$state, levels = names(state_effect))
say("respondents = %d, schools = %d, districts = %d, states = %d",
    nrow(d), length(unique(d$school)), length(unique(d$district)), nlevels(d$state))

m3 <- lmer(y ~ state + (1 | district) + (1 | district:school), data = d)
vc <- as.data.frame(VarCorr(m3))
est <- setNames(vc$vcov, c("school", "district", "student"))
print(data.frame(level = names(var_true), true = as.numeric(var_true),
                 estimate = round(as.numeric(est[names(var_true)]), 4)))
tot <- sum(est)
say("share of residual variance: district %.3f, school-within-district %.3f, student %.3f",
    est["district"] / tot, est["school"] / tot, est["student"] / tot)
say("ICC for two students in the same school (same district too) = %.3f",
    (est["district"] + est["school"]) / tot)
print(round(fixef(m3), 4))

rule("Part 2b. Dropping the district level moves its variance elsewhere")
m2 <- lmer(y ~ state + (1 | school), data = d)
print(VarCorr(m2), comp = "Variance")

rule("Part 2c. Ignoring nesting understates uncertainty")
ols <- lm(y ~ state, data = d)
se <- cbind(OLS = coef(summary(ols))[, "Std. Error"],
            multilevel = coef(summary(m3))[, "Std. Error"])
print(round(se, 4))
nbar <- nrow(d) / length(unique(d$school))
mbar <- nrow(d) / length(unique(d$district))
rho_d <- est["district"] / tot; rho_s <- est["school"] / tot
say("average respondents per school = %.1f, per district = %.1f", nbar, mbar)
say("two-level design effect 1 + (n-1)*ICC = %.2f (ignores district clustering)",
    1 + (nbar - 1) * (rho_d + rho_s))
say("three-level design effect 1 + (m-1)*rho_d + (n-1)*rho_s = %.2f",
    1 + (mbar - 1) * rho_d + (nbar - 1) * rho_s)
say("observed variance ratio for the state contrasts (multilevel/OLS SE)^2 = %.2f",
    mean((se[-1, "multilevel"] / se[-1, "OLS"])^2))
say("stateS2: true 0.30; estimate %.3f; OLS 95%% CI [%.3f, %.3f]; multilevel 95%% CI [%.3f, %.3f]",
    fixef(m3)["stateS2"],
    fixef(m3)["stateS2"] - 1.96 * se["stateS2", "OLS"], fixef(m3)["stateS2"] + 1.96 * se["stateS2", "OLS"],
    fixef(m3)["stateS2"] - 1.96 * se["stateS2", "multilevel"], fixef(m3)["stateS2"] + 1.96 * se["stateS2", "multilevel"])

rule("Part 2d. Shrinkage depends on how many students answered")
sch <- aggregate(y ~ school + district + state, data = d, FUN = mean)
sch$n <- as.numeric(table(d$school)[sch$school])
re_s <- ranef(m3)$`district:school`; re_d <- ranef(m3)$district
sch$predicted <- fixef(m3)[1] +
  ifelse(sch$state == "S2", fixef(m3)["stateS2"], 0) +
  ifelse(sch$state == "S3", fixef(m3)["stateS3"], 0) +
  re_d[sch$district, 1] + re_s[paste(sch$district, sch$school, sep = ":"), 1]
# Approximate reliability of one school's mean (school-level variance only).
sch$reliability <- est["school"] / (est["school"] + est["student"] / sch$n)
sch$gap <- abs(sch$y - mean(sch$y))
extreme <- function(k) { s <- sch[sch$n == k, ]; s[order(-s$gap), ][1:2, ] }
pick <- rbind(extreme(8), extreme(80))
print(transform(pick[, c("school", "n", "y", "predicted", "reliability")],
                y = round(y, 3), predicted = round(predicted, 3), reliability = round(reliability, 3)))
say("mean of all school means = %.3f", mean(sch$y))
say("Spread (SD) of raw school means = %.3f; of model predictions = %.3f",
    sd(sch$y), sd(sch$predicted))

rule("Part 2e. Within vs between: the contextual (Mundlak) effect")
set.seed(7)
schools <- 60; per <- 20
ses_school <- rnorm(schools, 0, 1)
dd <- data.frame(school = factor(rep(1:schools, each = per)))
dd$ses <- ses_school[dd$school] + rnorm(nrow(dd), 0, 1)
dd$y <- 0.2 * (dd$ses - ses_school[dd$school]) + 0.6 * ses_school[dd$school] +
  rnorm(schools, 0, 0.3)[dd$school] + rnorm(nrow(dd), 0, 1)
dd$ses_mean <- ave(dd$ses, dd$school)
dd$ses_within <- dd$ses - dd$ses_mean
say("true within-school slope 0.2; true between-school slope 0.6")
say("reliability of observed school-mean SES = 1/(1 + 1/%d) = %.3f (school SES var 1, within var 1)",
    per, 1 / (1 + 1 / per))
say("pooled OLS slope                  = %.3f", coef(lm(y ~ ses, dd))["ses"])
say("school fixed-effects slope        = %.3f", coef(lm(y ~ ses + school, dd))["ses"])
say("random intercept, raw ses         = %.3f", fixef(lmer(y ~ ses + (1 | school), dd))["ses"])
wb <- fixef(lmer(y ~ ses_within + ses_mean + (1 | school), dd))
say("within-between model: within = %.3f, between = %.3f, contextual = between - within = %.3f",
    wb["ses_within"], wb["ses_mean"], wb["ses_mean"] - wb["ses_within"])
