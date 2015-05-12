import pandas as pd
import statsmodels.formula.api as sm2
import statsmodels.api as sm

reader = pd.io.stata.StataReader('ships.dta')
df = reader.data()

dummies = df.ix[:, 0:3]
dummies = pd.concat([pd.get_dummies(dummies[col]) for col in dummies], axis=1, keys=df.columns)
dummies = pd.concat([dummies, df['months']], axis=1)
dummies['intercept'] = [1]*len(dummies)

dummies.columns = ['A', 'B', 'C', 'D', 'E',
                   'c1960-64', 'c1965-70', 'c1970-74',
                   'c1975-79', 'o1960-74', 'o1975-79',
                   'months', 'intercept']


poisson_glm = sm.GLM(df['damage'], dummies.drop(['A', 'c1960-64', 'o1960-74'], axis=1), family=sm.families.Poisson())
poisson_results = poisson_glm.fit()
# challenge 1 answers
#print poisson_results.summary()

#                  Generalized Linear Model Regression Results
# ==============================================================================
# Dep. Variable:                 damage   No. Observations:                   34
# Model:                            GLM   Df Residuals:                       24
# Model Family:                 Poisson   Df Model:                            9
# Link Function:                    log   Scale:                             1.0
# Method:                          IRLS   Log-Likelihood:                -84.182
# Date:                Thu, 07 May 2015   Deviance:                       70.498
# Time:                        16:39:29   Pearson chi2:                     65.8
# No. Iterations:                     9
# =================================================================================================
#                                     coef    std err          z      P>|z|      [95.0% Conf. Int.]
# -------------------------------------------------------------------------------------------------
# (u'type', u'A')                   0.4132      0.148      2.784      0.005         0.122     0.704
# (u'type', u'B')                   1.0832      0.156      6.952      0.000         0.778     1.389
# (u'type', u'C')                  -0.7784      0.246     -3.162      0.002        -1.261    -0.296
# (u'type', u'D')                  -0.4162      0.212     -1.964      0.050        -0.832    -0.001
# (u'type', u'E')                   0.2639      0.164      1.607      0.108        -0.058     0.586
# (u'construction', u'1960-64')    -0.7190      0.161     -4.479      0.000        -1.034    -0.404
# (u'construction', u'1965-70')     0.3683      0.088      4.203      0.000         0.197     0.540
# (u'construction', u'1970-74')     0.7809      0.098      7.958      0.000         0.589     0.973
# (u'construction', u'1975-79')     0.1355      0.152      0.892      0.372        -0.162     0.433
# (u'operation', u'1960-74')       -0.0813      0.087     -0.938      0.348        -0.251     0.089
# (u'operation', u'1975-79')        0.6471      0.061     10.620      0.000         0.528     0.766
# months                         6.697e-05   8.52e-06      7.857      0.000      5.03e-05  8.37e-05
# intercept                         0.5657      0.064      8.891      0.000         0.441     0.690
# =================================================================================================


#################################################################################
#################################################################################

# poisson_glm = sm2.glm(formula="damage ~ type + construction + operation", data=dummies, family=sm.families.Poisson(), offset=dummies['months'])
# poisson_results = poisson_glm.fit()
# # challenge 2 answers
# print poisson_results.summary()



poisson_glm = sm.GLM(df['damage'], dummies.drop(['A', 'c1960-64', 'o1960-74'], axis=1), family=sm.families.Poisson(), offset=dummies['months'])
poisson_results = poisson_glm.fit()
# challenge 2 answers
#print poisson_results.summary()

# >>>                  Generalized Linear Model Regression Results
# ==============================================================================
# Dep. Variable:                 damage   No. Observations:                   34
# Model:                            GLM   Df Residuals:                       24
# Model Family:                 Poisson   Df Model:                            9
# Link Function:                    log   Scale:                             1.0
# Method:                          IRLS   Log-Likelihood:                -84.182
# Date:                Thu, 07 May 2015   Deviance:                       70.498
# Time:                        17:32:25   Pearson chi2:                     65.8
# No. Iterations:                     9
# ==============================================================================
#                  coef    std err          z      P>|z|      [95.0% Conf. Int.]
# ------------------------------------------------------------------------------
# B              0.6701      0.217      3.085      0.002         0.244     1.096
# C             -1.1916      0.328     -3.638      0.000        -1.833    -0.550
# D             -0.8294      0.288     -2.883      0.004        -1.393    -0.266
# E             -0.1493      0.235     -0.636      0.525        -0.610     0.311
# c1965-70       1.0873      0.179      6.067      0.000         0.736     1.439
# c1970-74       1.4998      0.225      6.673      0.000         1.059     1.940
# c1975-79       0.8545      0.276      3.097      0.002         0.314     1.395
# o1975-79       0.7284      0.136      5.369      0.000         0.462     0.994
# months        -0.9999   8.52e-06  -1.17e+05      0.000        -1.000    -1.000
# intercept      0.1786      0.277      0.645      0.519        -0.364     0.722
# ==============================================================================


#################################################################################
#################################################################################

#challenge 3


