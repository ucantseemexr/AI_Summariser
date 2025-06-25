import textwrap
def build_adjustment_prompt(text: str, sections: list[dict], original_summary_by_section: dict) -> str:
    prompt = f"""You are a helpful summarization assistant.
Your task is to revise the original summary for each section strictly based on the provided adjustment instructions and input text.

⚠️ IMPORTANT RULES:
- DO NOT add any external knowledge or assumptions.
- DO NOT invent or modify section titles or subsections.
- ONLY use the content found in the provided passage.
- Follow the format in the example strictly.

{examples}

---

Now follow the same pattern. For each section, revise the summary according to the instruction. Do NOT change the meaning unless explicitly required.
"""

    for section in sections:
        title = section['title']
        
        prompt += f"""
=== Input Text ===
(Use only the content below to revise the summary. Do not include anything not in the text.)
{text.strip()}

=== Original Summary ===
{original_summary_by_section.get(title, '[original summary missing]').strip()}

=== Adjustment Instruction ===
{section['instruction']}

=== Revised Summary ===
"""

    return textwrap.dedent(prompt)

examples = f"""
=== Example 1 ===

=== Input Text ===
The American Civil War broke out in 1861 after decades of simmering tensions between Northern and Southern states over slavery, states’ rights, and economic differences. The election of Abraham Lincoln, who opposed the expansion of slavery, led Southern states to secede and form the Confederacy, prompting war.

=== Original Summary ===

The American Civil War was caused by long-standing tensions over slavery, states’ rights, and economic differences, culminating in the secession of Southern states following Abraham Lincoln’s election.

=== Adjustment Instruction ===
Reword the summary to be more concise and emphasize the political trigger.

=== Revised Summary ===

The Civil War stemmed from disputes over slavery, states' rights, and economics, triggered by Abraham Lincoln’s anti-slavery election that led Southern states to secede.
=== End of Output ===

=== Example 2 ===

=== Input Text ===
The moon landing in 1969 was a pivotal moment in human history, demonstrating the capabilities of space exploration and marking the United States' victory in the Space Race. Neil Armstrong became the first human to walk on the moon, which inspired generations of scientific and technological advancement.

=== Original Summary ===

The 1969 moon landing symbolized a major achievement in space exploration and American innovation, inspiring future technological progress and demonstrating the potential of human ingenuity.

=== Adjustment Instruction ===
Simplify the language and make it more accessible to high school students.

=== Revised Summary ===

The 1969 moon landing was a big step for science and America, showing that people could go to space and inspiring new inventions and technology.
=== End of Output ===

=== Example 3 ===

=== Input Text ===
A plant-based diet emphasizes whole grains, vegetables, fruits, legumes, nuts, and seeds while minimizing or eliminating animal products. Research shows that it can reduce the risk of chronic illnesses such as heart disease, type 2 diabetes, and certain cancers. It may also promote weight loss, improve digestion, and contribute to environmental sustainability.

=== Original Summary ===

A plant-based diet can reduce the risk of chronic diseases, promote healthy weight management, improve digestion, and support environmental sustainability.

=== Adjustment Instruction ===
Make the summary more detailed and use bullet points.

=== Revised Summary ===

- Reduces risk of heart disease, diabetes, and some cancers
- Helps manage body weight and digestion
- Benefits the environment by lowering emissions and conserving resources
=== End of Output ===

=== Example 4 ===

=== Input Text ===
Alcohol: Balancing Risks and Benefits
red wine being poured into a glass
Moderate drinking can be healthy—but not for everyone. You must weigh the risks and benefits.

–Introduction
–What’s Moderate Alcohol Intake? What’s a Drink?
–The Downside of Alcohol
–Possible Health Benefits of Alcohol
–Genes Play a Role
–Shifting Benefits and Risks
–The Bottom Line: Balancing Risks and Benefits

Introduction
Throughout the 10,000 or so years that humans have been drinking fermented beverages, they’ve also been arguing about their merits and demerits. The debate still simmers today, with a lively back-and-forth over whether alcohol is good for you or bad for you.

It’s safe to say that alcohol is both a tonic and a poison. The difference lies mostly in the dose. Moderate drinking seems to be good for the heart and circulatory system, and probably protects against type 2 diabetes and gallstones. Heavy drinking is a major cause of preventable death in most countries. In the U.S., alcohol is implicated in about half of fatal traffic accidents. [1] Heavy drinking can damage the liver and heart, harm an unborn child, increase the chances of developing breast and some other cancers, contribute to depression and violence, and interfere with relationships.

Alcohol’s two-faced nature shouldn’t come as a surprise. The active ingredient in alcoholic beverages, a simple molecule called ethanol, affects the body in many different ways. It directly influences the stomach, brain, heart, gallbladder, and liver. It affects levels of lipids (cholesterol and triglycerides) and insulin in the blood, as well as inflammation and coagulation. It also alters mood, concentration, and coordination.

What’s Moderate Alcohol Intake? What’s a Drink?
Loose use of the terms “moderate” and “a drink” has fueled some of the ongoing debate about alcohol’s impact on health.

In some studies, the term “moderate drinking” refers to less than 1 drink per day, while in others it means 3-4 drinks per day. Exactly what constitutes “a drink” is also fairly fluid. In fact, even among alcohol researchers, there’s no universally accepted standard drink definition. [2]

In the U.S., 1 drink is usually considered to be 12 ounces of beer, 5 ounces of wine, or 1½ ounces of spirits (hard liquor such as gin or whiskey). [3] Each delivers about 12 to 14 grams of alcohol on average, but there is a wider range now that microbrews and wine are being produced with higher alcohol content.

Is Red Wine Better?
Some experts have suggested that red wine makes the difference, but other research suggests that beverage choice appears to have little effect on cardiovascular benefit.
The definition of moderate drinking is something of a balancing act. Moderate drinking sits at the point at which the health benefits of alcohol clearly outweigh the risks.

The latest consensus places this point at no more than 1-2 drinks a day for men, and no more than 1 drink a day for women. This is the definition used by the U.S. Department of Agriculture and the Dietary Guidelines for Americans 2020-2025, [3] and is widely used in the United States.

The Dark Side of Alcohol
Not everyone who likes to drink alcohol stops at just one. While many people drink in moderation, some don’t.

Red wine splashing out of glass
Heavy drinking can take a toll on the body. It can cause inflammation of the liver (alcoholic hepatitis) and lead to scarring of the liver (cirrhosis), a potentially fatal disease. It can increase blood pressure and damage heart muscle (cardiomyopathy). Heavy alcohol use has also been linked with several cancers: The World Cancer Research Fund and American Institute for Cancer Research indicate that there is convincing evidence linking alcohol to cancers of the mouth, pharynx, larynx, esophagus, breast, liver, colon, and rectum. [4] The International Agency for Research on Cancer concluded that both the ethanol in alcohol and acetaldehyde, a chemical formed from the breakdown of ethanol, are carcinogenic to humans in high amounts. [5] The risk is multiplied for drinkers who also smoke tobacco or have a poor diet.

Problem drinking also touches drinkers’ families, friends, and communities. According to the National Institute on Alcohol Abuse and Alcoholism and others:

In 2014, about 61 million Americans were classified as binge alcohol users (5 or more drinks on the same occasion at least once a month) and 16 million as heavy alcohol users (5 or more drinks on the same occasion on 5 or more days in one month). [6]
Alcohol plays a role in one in three cases of violent crime. [7]
In 2015, more than 10,000 people died in automobile accidents in which alcohol was involved. [8]
Alcohol abuse costs about $249 billion a year. [9]
Even moderate drinking carries some risks. Alcohol can disrupt sleep and one’s better judgment. Alcohol interacts in potentially dangerous ways with a variety of medications, including acetaminophen, antidepressants, anticonvulsants, painkillers, and sedatives. It is also addictive, especially for people with a family history of alcoholism.

Alcohol Increases Risk of Developing Breast Cancer
There is convincing evidence that alcohol consumption increases the risk of breast cancer, and the more alcohol consumed, the greater the risk. [10-14]

A large prospective study following 88,084 women and 47,881 men for 30 years found that even 1 drink a day increased the risk of alcohol-related cancers (colorectum, female breast, oral cavity, pharynx, larynx, liver, esophagus) in women, but mainly breast cancer, among both smokers and nonsmokers. 1 to 2 drinks a day in men who did not smoke was not associated with an increased risk of alcohol-related cancers. [15] 
In a combined analysis of six large prospective studies involving more than 320,000 women, researchers found that having 2-5 drinks a day compared with no drinks increased the chances of developing breast cancer as high as 41%. It did not matter whether the form of alcohol was wine, beer, or hard liquor. [10] This doesn’t mean that 40% or so of women who have 2-5 drinks a day will get breast cancer. Instead, it is the difference between about 13 of every 100 women developing breast cancer during their lifetime—the current average risk in the U.S.—and 17 to 18 of every 100 women developing the disease. This modest increase would translate to significantly more women with breast cancer each year.
A lack of folate in the diet or folic acid, its supplement form, further increases the risk of breast cancer in women. [14] Folate is needed to produce new cells and to prevent changes in DNA. Folate deficiency, as can occur with heavy alcohol use, can cause changes in genes that may lead to cancer. Alcohol also increases estrogen levels, which fuel the growth of certain breast cancer cells. An adequate intake of folate, at least 400 micrograms a day, when taking at least 1 drink of alcohol daily appears to lessen this increased risk. [16, 17]

Researchers found a strong association among three factors—genetics, folate intake, and alcohol—in a cohort from the Nurses’ Health Study II of 2866 young women with an average age of 36 who were diagnosed with invasive breast cancer. Those with a family history of breast cancer who drank 10 grams or more of alcoholic beverages daily (equivalent to 1 or more drinks) and ate less than 400 micrograms of folate daily almost doubled their risk (1.8 times) of developing the cancer. Women who drank this amount of alcohol but did not have a family history of breast cancer and ate at least 400 micrograms of folate daily did not have an increased breast cancer risk. [14]
Folate and Alcohol
Alcohol and Weight Gain
Sugary mixed alcoholic beverage
One serving of alcohol on average contains 100-150 calories, so even a moderate amount of 3 drinks a day can contribute 300+ calories. Mixed drinks that add juice, tonic, or syrups will further drive up calories, increasing the risk of weight gain over time.

However, a prospective study following almost 15,000 men at four-year periods found only an increased risk of minor weight gain with higher intakes of alcohol. [19] Compared to those who did not change their alcohol intake, those who increased their intake by 2 or more drinks a day gained a little more than a half-pound. It was noted that calorie intake (not from alcohol) tended to increase along with alcohol intake.

Possible Health Benefits of Alcohol
What are some of the possible health benefits associated with moderate alcohol consumption?

Cardiovascular Disease
More than 100 prospective studies show an inverse association between light to moderate drinking and risk of heart attack, ischemic (clot-caused) stroke, peripheral vascular disease, sudden cardiac death, and death from all cardiovascular causes. [20] The effect is fairly consistent, corresponding to a 25-40% reduction in risk. However, increasing alcohol intake to more than 4 drinks a day can increase the risk of hypertension, abnormal heart rhythms, stroke, heart attack, and death. [5, 21-23]

Alcohol and Heart Disease: Prospective Studies
The connection between moderate drinking and lower risk of cardiovascular disease has been observed in men and women. It applies to people who do not have heart disease, and also to those at high risk for having a heart attack or stroke or dying of cardiovascular disease, including those with type 2 diabetes, [32, 33] high blood pressure, [34, 35] and existing cardiovascular disease. [34, 35] The benefits also extend to older individuals. [36]

The idea that moderate drinking protects against cardiovascular disease makes sense biologically and scientifically. Moderate amounts of alcohol raise levels of high-density lipoprotein (HDL, or “good” cholesterol), [37] and higher HDL levels are associated with greater protection against heart disease. Moderate alcohol consumption has also been linked with beneficial changes ranging from better sensitivity to insulin to improvements in factors that influence blood clotting, such as tissue type plasminogen activator, fibrinogen, clotting factor VII, and von Willebrand factor. [37] Such changes would tend to prevent the formation of small blood clots that can block arteries in the heart, neck, and brain, the ultimate cause of many heart attacks and the most common kind of stroke.

Drinking Patterns Matter
Glass of beer on a table
What you drink (beer or wine) doesn’t seem to be nearly as important as how you drink. Having 7 drinks on a Saturday night and then not drinking the rest of the week isn’t at all the equivalent of having 1 drink a day. The weekly total may be the same, but the health implications aren’t. Among participants in the Health Professionals Follow-up Study, consumption of alcohol on at least three or four days a week was inversely associated with the risk for myocardial infarction. The amount consumed, under 10 grams a day or more than 30 grams, didn’t seem to matter as much as the regularity of consumption. [25] A similar pattern was seen in Danish men. [38]

A review of alcohol consumption in women from the Nurses’ Health Study I and II found that smaller amounts of alcohol (about 1 drink per day) spread out over four or more days per week had the lowest death rates from any cause, compared with women who drank the same amount of alcohol but in one or two days. [39]

The most definitive way to investigate the effect of alcohol on cardiovascular disease would be with a large trial in which some volunteers were randomly assigned to have 1 or more alcoholic drinks a day and others had drinks that looked, tasted, and smelled like alcohol but were actually alcohol free. Many of these trials have been conducted for weeks, and in a few cases months and even up to 2 years, to look at changes in the blood, but a long-term trial to test experimentally the effects of alcohol on cardiovascular disease has not been done.  A recent successful effort in the U.S. to launch an international study was funded by the National Institutes of Health.  Although the proposal was peer-reviewed and initial participants had been randomized to drink in moderation or to abstain, post hoc the NIH decided to stop the trial due to internal policy concerns.  Unfortunately, a future long trial of alcohol and clinical outcomes may never be attempted again, but nevertheless, the connection between moderate drinking and cardiovascular disease almost certainly represents a cause-and-effect relationship based on all of the available evidence to date.

Beyond the Heart
The benefits of moderate drinking aren’t limited to the heart. In the Nurses’ Health Study, the Health Professionals Follow-up Study, and other studies, gallstones [40, 41] and type 2 diabetes [32, 42, 43] were less likely to occur in moderate drinkers than in non-drinkers. The emphasis here, as elsewhere, is on moderate drinking.

In a meta-analysis of 15 original prospective cohort studies that followed 369,862 participants for an average of 12 years, a 30% reduced risk of type 2 diabetes was found with moderate drinking (0.5-4 drinks a day), but no protective effect was found in those drinking either less or more than that amount. [32]

The social and psychological benefits of alcohol can’t be ignored. A drink before a meal can improve digestion or offer a soothing respite at the end of a stressful day; the occasional drink with friends can be a social tonic. These physical and social effects may also contribute to health and well-being.

Genes Play a Role
Twin, family, and adoption studies have firmly established that genetics plays an important role in determining an individual’s preferences for alcohol and his or her likelihood for developing alcoholism. Alcoholism doesn’t follow the simple rules of inheritance set out by Gregor Mendel. Instead, it is influenced by several genes that interact with each other and with environmental factors. [1]

There is also some evidence that genes influence how alcohol affects the cardiovascular system. An enzyme called alcohol dehydrogenase helps metabolize alcohol. One variant of this enzyme, called alcohol dehydrogenase type 1C (ADH1C), comes in two “flavors.” One quickly breaks down alcohol, the other does it more slowly. Moderate drinkers who have two copies of the gene for the slow-acting enzyme are at much lower risk for cardiovascular disease than moderate drinkers who have two genes for the fast-acting enzyme. [44] Those with one gene for the slow-acting enzyme and one for the faster enzyme fall in between.

It’s possible that the fast-acting enzyme breaks down alcohol before it can have a beneficial effect on HDL and clotting factors. Interestingly, these differences in the ADH1C gene do not influence the risk of heart disease among people who don’t drink alcohol. This adds strong indirect evidence that alcohol itself reduces heart disease risk.

Shifting Benefits and Risks
White wine being poured into a glass from a bottle
The benefits and risks of moderate drinking change over a lifetime. In general, risks exceed benefits until middle age, when cardiovascular disease begins to account for an increasingly large share of the burden of disease and death.

For a pregnant woman and her unborn child, a recovering alcoholic, a person with liver disease, and people taking one or more medications that interact with alcohol, moderate drinking offers little benefit and substantial risks.
For a 30-year-old man, the increased risk of alcohol-related accidents outweighs the possible heart-related benefits of moderate alcohol consumption.
For a 60-year-old man, a drink a day may offer protection against heart disease that is likely to outweigh potential harm (assuming he isn’t prone to alcoholism).
For a 60-year-old woman, the benefit/risk calculations are trickier. Ten times more women die each year from heart disease (460,000) than from breast cancer (41,000). However, studies show that women are far more afraid of developing breast cancer than heart disease, something that must be factored into the equation.
The Bottom Line: Balancing Risks and Benefits
Given the complexity of alcohol’s effects on the body and the complexity of the people who drink it, blanket recommendations about alcohol are out of the question. Because each of us has unique personal and family histories, alcohol offers each person a different spectrum of benefits and risks. Whether or not to drink alcohol, especially for “medicinal purposes,” requires careful balancing of these benefits and risks.

Your healthcare provider should be able to help you do this. Your overall health and risks for alcohol-associated conditions should factor into the equation.
If you are thin, physically active, don’t smoke, eat a healthy diet, and have no family history of heart disease, drinking alcohol won’t add much to decreasing your risk of cardiovascular disease.
If you don’t drink, there’s no need to start. You can get similar benefits with exercise (beginning to exercise if you don’t already or boosting the intensity and duration of your activity) or healthier eating.
If you are a man with no history of alcoholism who is at moderate to high risk for heart disease, a daily alcoholic drink could reduce that risk. Moderate drinking might be especially beneficial if you have low HDL that just won’t budge upward with diet and exercise.
If you are a woman with no history of alcoholism who is at moderate to high risk for heart disease, the possible benefits of a daily drink must be balanced against the small increase in risk of breast cancer.
If you already drink alcohol or plan to begin, keep it moderate—no more than 2 drinks a day for men or 1 drink a day for women. And make sure you get adequate amounts of folate, at least 400 micrograms a day.

=== Original Summary ===

1. Physical Health Risks
Liver damage: Can cause alcoholic hepatitis and cirrhosis.

Heart damage: Heavy drinking can lead to high blood pressure, irregular heart rhythms, and cardiomyopathy.

Cancer: Increases the risk of several cancers, including breast, mouth, throat, liver, esophagus, colon, and rectum.

Weight gain: Alcohol is calorie-dense (100–150 calories per drink) and can lead to weight gain, especially with sugary mixed drinks.

Sleep disruption and poor judgment.

2. Mental and Behavioral Risks
Addiction: Alcohol is addictive, especially for those with a family history of alcoholism.

Depression and violence: Linked to increased risk of mental health issues and aggressive behavior.

Increased risk of accidents: Alcohol is involved in about half of fatal traffic accidents in the U.S.

3. Increased Cancer Risk (Especially for Women)
Even one drink a day can increase the risk of breast cancer.

Risk is higher for women who drink 2–5 drinks a day and have low folate intake or a family history of breast cancer.

Alcohol raises estrogen levels, fueling hormone-sensitive breast cancers.

4. Social and Economic Impact
Family and community: Alcohol misuse can harm relationships and community safety.

Crime and accidents: One-third of violent crimes involve alcohol; over 10,000 alcohol-related road deaths in 2015.

Economic cost: Alcohol abuse costs the U.S. about $249 billion annually.

5. Medication Interactions
Alcohol can interact dangerously with medications like:

Painkillers

Antidepressants

Sedatives

Acetaminophen

6. Age and Situation-Specific Risks
Younger adults face higher risks from accidents and injuries.

Pregnant women, those with liver disease, or those on interacting medications should avoid alcohol entirely.

=== Adjustment Instruction ===
Expand the summary by adding categories and more concrete examples.

=== Revised Summary ===

1. Physical Health
- Liver: Risk of hepatitis and cirrhosis from heavy drinking.
- Heart: Can lead to high blood pressure and heart failure.
- Cancer: Alcohol is linked to breast, liver, colon, and throat cancers.
- Weight & Sleep: Causes weight gain and disrupts sleep.

2. Psychological & Behavioral
- Addiction risk, especially with family history.
- Linked to depression, aggression, and impaired judgment.
- Major contributor to fatal traffic accidents.

3. Female-Specific Cancer Risk
- One drink daily increases breast cancer risk, especially with low folate.
- Alcohol boosts estrogen levels, raising hormone-sensitive cancer risks.

4. Social & Economic Harm
- Hurts relationships, community safety, and causes crime.
- Costs U.S. $249B/year due to alcohol-related problems.

5. Drug Interactions
- Dangerous with antidepressants, sedatives, and painkillers.

6. Group-Specific Risk
- Pregnant women, people on medication, or with liver issues should abstain.
=== End of Output ===




=== End of Example ===
"""