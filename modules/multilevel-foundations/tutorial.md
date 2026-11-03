# Multilevel foundations: a refresher before psychometrics

Three topics, one idea: **variance lives at levels.** ANOVA splits variance into
within-group and between-group parts. Fixed and random effects are two ways of
treating the between-group part. A multilevel model does that split at every level
of nesting, such as students, schools, districts and states.

Every toy-data and simulation number below is printed by
[`multilevel_refresher.R`](multilevel_refresher.R) (seeded, R + lme4). Numbers quoted
from library sources are attributed inline. A few are short hand calculations from those
outputs, with the arithmetic shown. Run the script from the repository root and read along:

```powershell
Rscript modules/multilevel-foundations/multilevel_refresher.R
```

Notation: student $i$, school $j$, district $k$. $\sigma^2$ is within-school
(student-level) variance. $\tau^2$ is between-school variance. $n$ is respondents per school.

---

## 1. Analysis of variance: within and between

### The decomposition

Every score's distance from the grand mean splits into two pieces:

$$
\underbrace{y_{ij} - \bar y_{\cdot\cdot}}_{\text{total}}
= \underbrace{(\bar y_{\cdot j} - \bar y_{\cdot\cdot})}_{\text{between: school vs. everyone}}
+ \underbrace{(y_{ij} - \bar y_{\cdot j})}_{\text{within: student vs. own school}}
$$

Square and sum over everyone, and the cross-term vanishes:
$SS_\text{total} = SS_\text{between} + SS_\text{within}$.

### Worked toy example

Twelve students in three schools answer a 0–12 belonging scale:

| School | Scores | Mean |
|---|---|---|
| A | 4, 6, 8, 10 | 7 |
| B | 2, 4, 6, 8 | 5 |
| C | 5, 7, 9, 11 | 8 |

Grand mean = 6.667.

| Source | SS | df | MS = SS/df |
|---|---|---|---|
| Between schools | $4[(7-6.67)^2 + (5-6.67)^2 + (8-6.67)^2] = 18.67$ | $J-1 = 2$ | 9.33 |
| Within schools | each school contributes 20 → 60.00 | $J(n-1) = 9$ | 6.67 |
| Total | 78.67 | 11 | |

$F = 9.33 / 6.67 = 1.40$, $p = .30$.

### What the mean squares estimate (the part people forget)

The F-test is a comparison of two estimates of variance:

$$
E[MS_\text{within}] = \sigma^2 \qquad
E[MS_\text{between}] = \sigma^2 + n\,\tau^2
$$

$MS_\text{between}$ is inflated by noise ($\sigma^2$) even when schools don't differ at all
($\tau^2 = 0$). That is why $F \approx 1$ under the null hypothesis. Solve for the variance components:

$$
\hat\tau^2 = \frac{MS_B - MS_W}{n} = \frac{9.33 - 6.67}{4} = 0.667
\qquad \hat\sigma^2 = MS_W = 6.667
$$

**The key identity.** The variance of the observed school means is *not* the
variance of true school differences:

$$
\operatorname{Var}(\bar y_{\cdot j}) = \tau^2 + \frac{\sigma^2}{n}
\qquad\Rightarrow\qquad 2.333 = 0.667 + \tfrac{6.667}{4}
$$

At the point estimates, 71% of the spread in the three school means is sampling noise
from having only four respondents per school. With three schools and $p = .30$, $\tau^2$
could plausibly be 0, which would make the spread 100% noise. Raw school-mean dashboards
treat all of the spread as real.

Snijders & Bosker (2012, Example 3.1) make the point with random digits. They put 100
random digits into 10 rows of 10 and call each row a "school." The row means vary
(variance 105.7) and look like real school differences, although the true
between-school variance is exactly zero.

The estimator $(MS_B - MS_W)/n$ can come out negative when school means vary less than
chance alone would produce. Report it as 0 (§3.3.1). `lmer` does this automatically
and flags a *singular fit*.

### Intraclass correlation (ICC)

$$
\rho = \frac{\tau^2}{\tau^2 + \sigma^2} = \frac{0.667}{7.333} = 0.091
$$

Two equivalent readings:
- the share of total variance that lies between schools;
- the correlation between two students drawn from the same school.

Reference values from your library:

| Outcome | ICC | Source |
|---|---|---|
| Achievement in US schools | often 0.10–0.25 | Snijders & Bosker (2012, §3.3), citing Hedges & Hedberg (2007) |
| Reading scores (S052 example) | 77.04 / (77.04 + 314.19) = 0.197 | Ho, S052 Week 10 |
| Teacher (WCS) and student (Tripod) climate-survey *items* | ~0.06–0.27 | Schweig (2014) |
| 5Essentials screening threshold for a school-level measure | ICC > 0.05 | Hart et al. (2020), citing Hedberg & Hedges (2014) |

Small ICCs still matter a great deal, as Section 3 shows.

> **Bridge to measurement.** $\tau^2$ plays the part of true-score variance and
> $\sigma^2/n$ the part of error variance. So $\tau^2/(\tau^2+\sigma^2/n)$ is a
> *reliability coefficient*: the reliability of a school's mean. Snijders &
> Bosker (2012, §3.5) say this directly: when a school's climate is measured by its
> students' answers, "the micro-level units *i* are regarded as parallel items for
> measuring the macro-level unit *j*."
>
> Ho (S052 Week 11) uses the same model for *raters nested in teachers*.
> With teacher variance .051 and rater variance .225, one rater gives reliability .184,
> and an average of four raters gives .051 / (.051 + .225/4) = .474. A survey works
> the same way, with respondents in place of raters.
>
> Inverting the formula gives the number of respondents needed for a target
> reliability $\lambda_0$ (Snijders & Bosker, 2012, §11.3):
> $n_\text{min} = \lambda_0(1-\rho) / [(1-\lambda_0)\rho]$.
>
> | School ICC | Reliability .70 | Reliability .80 |
> |---|---|---|
> | .10 | 21 respondents | 36 respondents |
> | .05 | 45 respondents (44.3, rounded up) | 76 respondents |
>
> Hold onto this. It comes back in Sections 2, 3 and 4.

---

## 2. Fixed effects and random effects

### First, the terminology trap

"Fixed" and "random" mean different things in different fields. Most confusion
comes from switching meanings mid-sentence. Gelman (2005) catalogs five
inconsistent definitions. Three matter here:

| Usage | "Fixed effect" means | "Random effect" means |
|---|---|---|
| Classical ANOVA / multilevel (Snijders & Bosker) | each school's effect is its own parameter, estimated separately | school effects are draws from a distribution; you estimate the distribution's variance $\tau^2$ |
| Econometrics (panel data) | the *within* estimator: school dummies absorb every school-level confounder | assumes school effects are uncorrelated with predictors; biased if that fails |
| Software output (`lme4`, Stata `mixed`) | the regression coefficients $\gamma$ (population averages) | the variance components and the per-school deviations |

So a "random-intercept model" has "fixed effects" in its output. That is not a
contradiction; it is the third row.

### The same equation, two interpretations

$$
y_{ij} = \gamma_0 + u_j + e_{ij}, \qquad e_{ij} \sim N(0, \sigma^2)
$$

- **Fixed:** $u_j$ are $J$ unknown constants (with one constraint). This is `lm(y ~ school)`.
  Each school's estimate is its own raw mean.
- **Random:** $u_j \sim N(0, \tau^2)$, independent of $e_{ij}$. This is `lmer(y ~ 1 + (1|school))`.
  It has **one** extra parameter, $\tau^2$, not $J$ of them.

Ho (S052 Week 10) gives a compact framing. Fixed effects **eliminate**
between-group variance: they control it away so you can study within-school
relationships. Random effects **estimate and explain** it: they measure how large
it is, then let school-level variables account for part of it.

### Consequence 1: shrinkage (partial pooling)

The random-effects prediction for a school is a weighted average of its own mean
and the overall mean:

$$
\hat\mu_j = \lambda_j\,\bar y_{\cdot j} + (1-\lambda_j)\,\hat\gamma_0,
\qquad \lambda_j = \frac{\tau^2}{\tau^2 + \sigma^2/n_j}
$$

For the toy data, $\lambda = 0.667/(0.667 + 6.667/4) = 0.286$:

| School | Raw mean (fixed) | Random-effects prediction |
|---|---|---|
| A | 7 | 6.762 |
| B | 5 | 6.191 |
| C | 8 | 7.048 |

$\lambda_j$ is exactly the reliability of school $j$'s mean from Section 1. Shrinkage is
**Kelley's regressed true-score estimate** from classical test theory,
$\hat T = \rho X + (1-\rho)\mu$, applied to schools instead of examinees.
Unreliable means (few respondents) get pulled hard toward the center, while reliable
ones barely move. The result is called the Empirical Bayes estimate, BLUP, or posterior mean.

### Consequence 2: only random effects can use school-level predictors

Add `program` (schools A and C have it; B doesn't):

```
lm(y ~ school + program)      ->  program = NA   (perfectly collinear with school dummies)
lmer(y ~ program + (1|school)) ->  program = 2.5
```

The school dummies already "explain" all between-school variance, so nothing is
left for a school-level variable. Snijders & Bosker (2012, §4.3.1) put it this way:
"random effects" and "unexplained variability" are two names for the same thing.

Ho (S052 Week 9) shows the practical cost. A school fixed-effects model cannot
analyze a cluster-randomized trial, because the treatment is assigned to whole
schools and the dummies absorb it.

The script also reports a *singular fit* there. With `program` in the model,
the remaining school variance is estimated at 0, and three schools cannot say more.

### Consequence 3: the econometric worry and the Mundlak fix

*Optional on a first read. Come back once Consequences 1 and 2 feel solid.*

The random-intercept model assumes $u_j$ is uncorrelated with the predictors. In
school data it often isn't: high-SES schools differ in unmeasured ways. A simpler
version of the same problem is a within-school relationship that differs from the
between-school one. Part 2e of the script simulates a within-school SES slope of 0.2
and a between-school slope of 0.6. The school random effect is generated independently
of SES:

| Model | SES slope |
|---|---|
| Pooled OLS (ignore schools) | 0.367 (blend, wrong for both questions) |
| School fixed effects | 0.183 (≈ within slope only) |
| Random intercept, raw SES | 0.256 (another blend) |
| Random intercept with SES split into within + school mean | within 0.183, between 0.533 |

Add the school mean of the predictor (Mundlak; "within-between" models). The random-effects
model then recovers the fixed-effects within-slope *and* keeps the between-slope.
The between-minus-within difference (0.350 here) is the **contextual effect**. It is the
difference in expected outcome between two students with the same SES who attend schools
whose mean SES differs by one unit. Read it descriptively. It is a causal "the school adds
this" effect only if nothing else unmeasured about schools travels with school-mean SES.

Correlation between $u_j$ and a *student-level* predictor therefore doesn't force you
into fixed effects (Snijders & Bosker, 2012, §4.6; Ho, S052 Week 10). The school-mean
term does **not** protect coefficients of *school-level* predictors such as `program`
or Title I status. If $u_j$ correlates with those, their estimates are still biased.

Why is the between estimate 0.533 rather than 0.6? The observed school-mean SES is an
average of 20 students, so it contains sampling error. Its reliability here is
1 / (1 + 1/20) ≈ 0.95. An unreliable predictor pulls the between slope toward the within
slope, and sampling noise across only 60 schools adds the rest. Section 4 returns to
this problem (Marsh et al., 2009). Ignoring the distinction risks the **ecological fallacy**, which
reads a between-school relationship as if it held for individual students.

### Choosing

Rule of thumb from Snijders & Bosker (2012, §4.3.1):
- **Fewer than ~10 groups, or groups are unique categories you care about
  individually** (gender, these three states): treat them as fixed.
- **20+ groups seen as a sample from a population, modest $n_j$, and you want
  group-level predictors or $\tau^2$**: treat them as random.
- **10–20 groups:** ambiguous.
- **All $n_j \geq 100$:** the choice matters little for the *regression coefficients*,
  provided within and between effects are separated. School predictions still shrink at
  survey-typical ICCs. At ICC .05 and $n = 100$, $\lambda = 0.84$.

---

## 3. Multilevel models for school survey data

### The nesting and the model

Respondents $i$ sit in schools $j$, which sit in districts $k$, which sit in states $s$.
With only a handful of states, follow the rule above: states are **fixed**, and
districts and schools are **random**:

$$
y_{ijk} = \gamma_0 + \gamma_s\,[\text{state}] + v_k + u_{jk} + e_{ijk},
\qquad v_k \sim N(0,\phi^2),\; u_{jk} \sim N(0,\tau^2),\; e_{ijk} \sim N(0,\sigma^2)
$$

```r
lmer(y ~ state + (1 | district) + (1 | district:school), data = d)
```

`district:school` makes school IDs unique within districts. If school IDs are
already globally unique, `(1 | school)` is the same model.

### Simulation (Part 2 of the script)

The simulation has 3 states × 12 districts, 2–6 schools per district, and 8–80 respondents
per school: 4,798 respondents in 141 schools and 36 districts.

| Level | True variance | Estimated | Share |
|---|---|---|---|
| District | 0.040 | 0.044 | 4.3% |
| School (within district) | 0.060 | 0.058 | 5.8% |
| Student (within school) | 0.900 | 0.912 | 89.9% |

Three numbers come out of this table. Keep them apart, because formulas need different ones:

| Symbol | Value | Meaning |
|---|---|---|
| $\rho_3$ | 0.043 | district share of variance; also the correlation of two students in *different* schools of the same district |
| $\rho_2$ | 0.058 | school-*within-district* share of variance |
| $\rho_3 + \rho_2$ | 0.101 | correlation of two students in the *same* school |

This matches Hedges & Hedberg's definitions: their $\rho_2$ is the school-within-district
share, not the same-school correlation.
Their grade 3–8 achievement data averaged $\rho_3 \approx 0.05$ and
$\rho_2 \approx 0.10$–$0.13$. The simulation's school share (0.058) is lower than that.
Survey constructs vary, so estimate your own values rather than borrowing these.

### Why a 10% ICC is not ignorable

Part 2c compares the state-contrast standard errors:

| | OLS (ignores nesting) | Multilevel |
|---|---|---|
| SE, state S2 vs S1 | 0.035 | 0.109 |
| 95% CI for S2 (truth 0.30) | [0.079, 0.218] (**misses truth**) | [−0.065, 0.362] |

The **design effect** quantifies the cost of clustering (Snijders & Bosker, 2012, §3.4).
With $n$ respondents per school and $m$ per district, the two-level formula is the book's.
The three-level version is derived here from
$\operatorname{Var}(\bar y_k) = \phi^2 + \tau^2/(\text{schools}) + \sigma^2/m$:

$$
\text{deff}_{2\text{-level}} = 1 + (n-1)\rho = 1 + 33(0.101) = 4.33
$$
$$
\text{deff}_{3\text{-level}} = 1 + (m-1)\rho_3 + (n-1)\rho_2 = 1 + 132.3(0.043) + 33(0.058) \approx 8.64
$$

The two-level formula uses the same-school correlation (0.101). The three-level formula
uses $\rho_2$ (0.058), because the district term already counts the district share.

The observed variance ratio of the multilevel and OLS standard errors is 9.55. Both
formulas assume equal cluster sizes, and the standard errors are themselves estimates,
so treat 8.64 and 9.55 as the same order of magnitude rather than an exact match.
The lesson, using the observed ratio (4,798 / 9.55 ≈ 500): 4,798 respondents carry roughly
the information of 500 independent ones for a state comparison. The relevant sample size is driven by the number of
**districts**, not respondents.

### Omitting a level doesn't delete its variance

Drop districts (Part 2b) and fit only schools. The school variance becomes 0.099,
which is the district and school variances combined. The variance doesn't disappear;
it moves to the nearest included level. Snijders & Bosker (2012, §4.9) note this
also distorts tests of predictors at the omitted level.

### Shrinkage with uneven response counts

Each row below is one of the most extreme schools at that sample size (Part 2d):

| School | n | Raw mean | Model prediction | Reliability λ (approx.) |
|---|---|---|---|---|
| S1-6-2 | 8 | 3.891 | 3.547 | 0.34 |
| S1-4-3 | 8 | 2.233 | 2.467 | 0.34 |
| S1-11-3 | 80 | 2.191 | 2.327 | 0.84 |
| S1-4-5 | 80 | 1.954 | 2.058 | 0.84 |

Schools with eight respondents move 0.23–0.34 points toward their district/state
prediction; schools with eighty move 0.10–0.14. Overall, the SD of school predictions
(0.316) is smaller than the SD of raw means (0.397).

This has consequences for school reports. A school-level dashboard of raw means
over-rewards and over-punishes small schools. Shrunken estimates are fairer for
ranking, but they are pulled toward the district. Say which one you report.

### Practical checklist for survey data

1. **Count units at every level.** States are few, so treat them as fixed. Districts with one
   school can't separate district from school variance; they still contribute to the
   total, but the split rests on multi-school districts.
2. **Fit the empty model first** and report variance shares and ICCs at each level.
3. **Center deliberately.** Group-mean centering gives the within effect. Add the group
   mean to get the between and contextual effects.
4. **Respect response counts.** Small $n_j$ means low reliability of school means, so shrink or
   flag them. Don't rank schools on raw means.
5. **Item type.** A scale score averaged over items is roughly continuous, so a linear mixed model
   is reasonable. A single 4- or 5-point item is ordinal; use a cumulative-link
   mixed model (`ordinal::clmm`) or treat it with caution.
6. **Not everything nests.** Students who change schools and teachers who teach in two schools
   are *cross-classified*: `(1|school) + (1|neighborhood)` rather than nested terms.
7. **Sampling weights** (Snijders & Bosker, 2012, ch. 14).
   - Weights matter for model parameters only when the design is *informative*, meaning the
     residuals relate to the selection probabilities. Adding the design variables as
     predictors often makes it noninformative.
   - If you do weight, you need level-specific weights. The default `lmer` fit ignores them.
   - Design-based multilevel standard errors are unreliable with few clusters. Published
     simulations support good coverage only from about 100 clusters of 50.
8. **Census, not sample.** Staff surveys often invite *everyone* in a school. This does
   not remove the reliability problem for perception scales. For a reflective construct
   such as climate as perceived by staff, each respondent is a rater, and within-school
   disagreement is rater error even when everyone answers. Reliability, shrinkage and
   $n_\text{min}$ still apply.

   Marsh et al. (2009) raise a separate caution about *formative* aggregates, such as
   percent female or mean SES, which describe the school's composition. As the sampling
   ratio approaches 100%, latent aggregation may overestimate sampling error for those
   and inflate contextual effects. They call for more research on that case.
9. **Robust-SE alternative.** OLS with cluster-robust (sandwich) standard errors,
   clustered at the *highest* level (districts here), protects inference about fixed
   effects. It gives no variance components or school predictions, and it needs many
   clusters (Snijders & Bosker, 2012, §12.2).

---

## 4. Bridge to the psychometrics unit

The next unit asks you to defend a cross-group comparison under a measurement
model. Three links carry over directly:

- **A random intercept is a latent variable.** $u_j$ is an unobserved school
  trait that every student in school $j$ "loads on" with weight 1. A random-intercept
  model is a one-factor model with every loading fixed at 1, and multilevel and SEM
  frameworks can express each other (Mehta & Neale, 2005). This equivalence is
  established; how far to exploit it is a modeling choice.
- **Reliability of aggregates.** $\lambda_j$ is the reliability of a school mean.
  Marsh et al. (2009), following Bliese (2000), call it ICC(2): "the reliability of the
  group mean in relation to sampling error." Claims about *school* climate need this
  reliability, not the student-level α.
- **Two kinds of error, two kinds of "latent."** Marsh et al. (2009) cross two choices:
  - *measurement* error from sampling items, handled with multiple indicators (CFA/SEM);
  - *sampling* error from sampling people within schools, handled with latent aggregation
    (multilevel).

  The usual practice of averaging items and then averaging students is "doubly manifest"
  and corrects neither. An unreliable observed school mean biases the contextual effect
  from Part 2e. The doubly latent model corrects both errors but can be unstable with
  few or small groups, so compare the variants.
- **Constructs can differ by level.** Schweig (2014) found:
  - a teacher working-conditions survey with six factors within schools but five between them;
  - the Tripod student survey with five factors within classrooms but only two between them.

  An ordinary factor analysis of the pooled data reproduced the *within* structure and
  matched neither between-level structure. Cronbach (1976), quoted there, said that whether
  within- and between-group constructs coincide is "a possibility to be evaluated, not
  assumed." Cross-level invariance ($\Lambda_B = \Lambda_W$) is the multilevel form of the
  measurement-invariance question in the next unit: is the same thing measured at every
  level and in every group?

---

## Self-check

Try each question before opening the answers.

1. A district report shows school means ranging 2.2 to 3.9 on a 5-point scale. Some
   schools have 8 respondents. What must you know before calling the range "school differences"?
2. Why can't `lm(y ~ school + title1_status)` estimate the Title I effect?
3. Your ICC is 0.05 and you have 50 students per school. Roughly how much does
   clustering inflate the variance of an overall mean?
4. A colleague fits random school intercepts with student SES and reports a
   single SES slope. What is ambiguous about it, and how do you fix it?
5. You have 4 states, 40 districts, 300 schools. Which levels are random?

<details>
<summary>Answers</summary>

1. The within-school variance and each school's $n$. Observed spread is
   $\tau^2 + \sigma^2/n$, so part of the range is noise. Estimate $\tau^2$ and report shrunken
   estimates or reliabilities.
2. Title I status is constant within school, so it is perfectly collinear with the school
   dummies. Use a random intercept for school.
3. deff = 1 + 49(0.05) ≈ 3.45, so the effective sample size is about 29% of the nominal one.
4. The slope blends within- and between-school relationships, and it is biased if school
   effects correlate with SES. Add school-mean SES (Mundlak / within-between).
5. Districts and schools are random. Four states is too few to estimate a variance, so use fixed state effects.

</details>

---

## Sources

### Reading path (all in niu-library; passages inspected for this tutorial)

| Tutorial section | Read next |
|---|---|
| 1. Within/between, ICC | Snijders & Bosker ch. 3 (§3.3 random digits, §3.4 design effects, §3.5 reliability of aggregates); Ho S052 Week 9 Emphasis "Variance Within and Between" |
| 2. Fixed vs random, shrinkage, Mundlak | Snijders & Bosker §4.3, §4.6, §4.8; Ho S052 Week 9 Launch (random effects, ICCs), Week 10 Launch and 10.1 Supplement (Mundlak, REWB), Week 10 Emphasis (cross-level interactions, BLUPs) |
| 3. School surveys, three levels | Snijders & Bosker §4.9 (three-level), ch. 11 (design), §12.2 (sandwich SEs), ch. 14 (survey weights); Hedges & Hedberg (district/school ICCs); Lumley, *Complex Surveys* (design-based analysis) |
| 4. Bridge to psychometrics | Ho S052 Week 11 (measurement, imprecision, reliability); Ho & Kane (2013), raters as a variance component; Marsh et al. (2009); Schweig (2014); Mair, *Modern Psychometrics with R* |
| Applied school-survey examples | Hart et al. (2020) 5Essentials reexamination; Koth, Bradshaw & Leaf, multilevel predictors of school climate; Jones & Fleming (2021) |

### References

From niu-library, with the passages quoted or paraphrased above inspected:

- Snijders, T. A. B., & Bosker, R. J. (2012). *Multilevel Analysis* (2nd ed.). Sage.
- Ho, A. D. *S052: Applied Data Analysis* (Harvard GSE, 2023), Weeks 9–11 slides and supplements.
- Hedges, L. V., & Hedberg, E. C. *Intraclass Correlations and Covariate Outcome
  Correlations for Planning 2 and 3 Level Cluster Randomized Experiments in Education.*
- Marsh, H. W., Lüdtke, O., Robitzsch, A., Trautwein, U., Asparouhov, T., Muthén, B., &
  Nagengast, B. (2009). Doubly-latent models of school contextual effects. *Multivariate
  Behavioral Research.*
- Schweig, J. (2014). Cross-level measurement invariance in school and classroom
  environment surveys. *Educational Evaluation and Policy Analysis.*
- Hart, H., Young, C., Chen, A., Zou, A., & Allensworth, E. M. (2020). *Supporting School
  Improvement: Early Findings from a Reexamination of the 5Essentials Survey.* UChicago Consortium.

Listed in the reading path but not opened for this tutorial: Lumley (2010), Mair (2018),
Ho & Kane (2013), Koth et al., Jones & Fleming (2021).

Cited from general knowledge, not checked against the library in this session:
Gelman (2005), "Analysis of variance — why it is more important than ever," *Annals of
Statistics* (the five definitions); Mehta & Neale (2005), "People are variables too,"
*Psychological Methods*; Kelley (1927) on regressed true scores.
