from openpyxl import Workbook
import openpyxl

flavors = [
    "Social",
    "Environmental",
    "Economic",
    "Political",
    "Educational",
    "Innovative process",
]

angles = {
    "Level of Analysis": ["Micro", "Meso", "Macro"],
    "Spatial scope": ["Local", "Regional", "National or International"],
    "Time Horizon": ["1 year", "5 years", "25 years"],
}

CERNA = """## Climate and Energy Related Norms and Attitudes assessment
 
When it comes to supporting people in adapting their behaviour and making more sustainable, climate-friendly and energy efficient choices, providing information alone is rarely sufficient (Cadario & Chandon, 2020). Humans' perception is not solely influenced by information, but it is generally agreed upon that a myriad of heuristics effect our decisions unnoticed, every day. These are strategies that use only a small fraction of the available information. This makes our decision very rapid, which is incredibly useful in evolutionary terms, to survive approaching danger, for instance. Fortunately, most of the time the result of using automatic heuristic thinking is “good enough”, however in certain situations they lead to poor judgments. We might think of these as “errors in judgement” while in psychological literature they are commonly known as cognitive biases (Ellis, 2018).
Certain cognitive biases, e.g., the false consensus effect (our tendency to overestimate how many people agree with our own beliefs), the misinformation effect (our memory of events is heavily influenced by how that event is represented, for example in media), the availability heuristic (our tendency of estimating the probability of something based on the examples that we are aware of), or the optimism bias (underestimating the probability of bad things happening to us but overestimating the good) are all factors we need to consider and address when we would like to change energy and environment related behaviour. (Zhang et al., 2020) With the below proposed social and behavioural research and innovation approaches we aim to make sure that all aspects of human cognition are taken into consideration before a top-down intervention would be forced on the public – which might be ineffective or even polarizing.
Awareness, however, is undoubtedly the first step to the adaptation of more sustainable behaviours. (Park et al., 2023). Public engagement is a two-way dialogue. Before intervening, we need to listen; assess knowledge and attitudes, understand interests and barriers to action through social scientific research. This will inform us about our starting point and allow us to plan meaningful interventions, targeted at the identified gaps in public understanding on climate issues.
For these purposes we propose to administer a Climate and Energy Related Norms and Attitudes (CERNA) survey in all six PROBONO Living Labs. In the absence of a comprehensive and suitable tool, the survey will be created by Smart Innovation Norway, inspired by available literature on Energy literacy assessment, Climate Change literacy assessment, and assessment on Pluralistic Ignorance related to climate issues.
Energy literacy assessment
 
Energy literacy is defined as the indicator of basic energy-related knowledge, the understanding of the environmental impacts of energy production and consumption, how energy is used and the adoption of energy-saving behaviours. This definition works with three dimensions: knowledge, attitudes, and behaviours (DeWaters & Powers, 2011).
The knowledge component refers to the understanding of basic scientific concepts, rules, theories, and the role and usage of energy in our everyday lives. The attitude refers to the ideologies and convictions of each person, based on their energy knowledge, influencing their decision-making processes. The behavioural component evaluates awareness of the impact of day-to-day actions, and each individual’s responsibility and the commitment to save energy (Martins, Madaleno & Dias, 2020). It is important to note however that self-reported behaviours have proven to be unreliable in several examples (Hansen, Larsen & Gundersen, 2021; Kormos & Gifford, 2014), hence our approach is to utilize behavioural insights, where behaviour change will be monitored instead of inquired about.
In the interest of being able to design practical interventions for the Living Labs based on the data gathered here, our survey will work with all these three components, but will focus less on the scientific and theoretical knowledge, and more on the awareness of the efficient ways to save energy in terms of day-to-day practices of everyday life. Existing research suggests that people tend to overweigh the value of easier, more salient actions, e.g., turning off the lights, compared to other energy saving actions that in reality are significantly more effective, like reducing temperature and length of showers (Park et al., 2023). With this survey, we aim to find out, whether there are such misconceptions to address in the PROBONO Living Labs. This would open the door to a wide range of interventions, that, although of minimal effort, can bring significant improvements in energy behaviour. It could inform not only the content but also the timing and adequate context of the communication. Examples of targeted communications depending on our findings could be nudging stickers on household appliances, policy recommendations on different labelling of certain products, providing households with “energy toolkits” containing helpful information and tools, etc.
Climate change literacy assessment
 
Climate change is a complex issue which requires understanding the basic principles of multidisciplinary scientific principles of physics, chemistry, geography, biology and mathematics (Anyanwu, Le Grange & Beets, 2015). For this reason, it is an unobtrusive, diffused, non-localised issue for many. Even for individuals who personally experience the effects of climate change, it is often unclear, whether they can be attributed to climate change or not, not to mention that many are unaware of the scientific consensus on anthropogenic climate change (Geiger, Gruszczynski & Swim, 2022).
Similarly to energy literacy assessment, the available tools on climate change literacy assessment focus on scientific understanding of the phenomena. We instead propose to measure the awareness of the anthropogenic causes, the impacts, and possible solutions. We will measure the attitudes, concerns, or potential scepticism, to make sure that we can provide customized engagement suggestions to each Living Labs.
Pluralistic ignorance assessment
 
The aim of the Climate and Energy Related Norms and Attitudes survey is to assess not only factual knowledge, but assumptions as well on other peoples’ knowledge and attitudes. Social cognition research suggests that human behaviour is dependent on our subjective representation of reality, which is influenced by our perception and interpretation of surrounding. Our decisions and actions are largely influenced by what we perceive is the “social norm”, especially if that is perceived as the norm of a group we strongly identify with (national, political, generational, etc.) (Farrow, Grolleau & Ibanez, 2017). When it comes to environmental issues, the underestimation of interest and awareness of our peers can be a huge barrier to action.
The literature calls this phenomenon pluralistic ignorance, which is a shared misconception on how others think or act (Park et al., 2023). According to a recent study, people vastly underestimate the public support for climate policies, and climate concern. While two thirds of the participants supported the policies, they estimated the supporters to be only one third of the population. Even though supporters of the climate action outnumber opponents two-to-one, these results have concerning implications. First, the underestimation of public willingness to discuss climate issues obstruct actions and behaviour change - in democratic models of governance, politicians are unlikely to propose climate actions without public support (Walker, Kurz & Russel, 2018). Second, overestimation of opposition to climate policies pressures us to oppose them as well, diminishing motivations towards the green transition. The absence of knowledge on the consensus around environmental issues gives way to polarization, which means these misperceptions will bring a self-fulfilling prophecy: not realizing the true level of support of climate action may in fact lead to decreased support in the future (Sparkman, Geiger & Weber, 2022).
Social norm interventions have been shown to be effective in reducing energy consumption in field experiments. The use of social norms in information provision, (informing people about others’ behaviours and attitudes), and other types of peer influence interventions could be leveraged by policy makers to target pro-environmental attitudes (Farrow, Grolleau & Ibanez, 2017).
As Hansen (2018) pointed out, when it comes to addressing behaviour changes and policy making, before intervening, a precise diagnosis of the problem will no doubt increase the success of said interventions. Merely treating symptoms may have short-term effects (with potential side effects) but also likely to lead to the regression to the status quo on the long run. With the above described three-component Climate and Energy Related Norms and Attitudes survey we propose a diagnostic approach to a wide range of factors that influence environment and energy related behaviour. Understanding this if the first step to ensure that the planned interventions will be beneficial and understood by the targeted communities, and future policies will maximise their potential.
GBN Contribution
An evidence-based approach to building behavioural changes and promoting pro-environmental social norms is a key aspect of building a Green Building Neighbourhood. The neighbourhood is to be developed with the people, for the people  - thus any meaningful change has to prioritise the community’s participation and willingness to adapt."""


def createBackground(flavor, angle):
    background = (
        """# Background
You are an international expert in behavioral science and social innovation.
You are part of a team of experts working on the assessment of a social innovation, which is detailed below. You role is to provide a concise but very accurate assessment of the text.
You will given a "flavor" (as part of the PESTLE framework), as well as an "angle" to do this review.
For now, the "flavor" will be to do your assessment considering the '"""
        + flavor
        + """' flavor, and you will want to consider the """
        + angle
        + """ angle.

# Expected answer
You will need to start your answer as a single line, starting with a '*' bulletpoint, containing only one of the following items: '"""
        + ", ".join(angles[angle])
        + """'. This item should be the scale that is the most relevant for the """
        + angle
        + """ angle.
Then, add another bulletpoint, and write a short (up to 3 sentences) detailing as much as you can the content of the social innovation considering the '"""
        + flavor
        + """' flavor and the '"""
        + angle
        + """' angle. It must not start with "The text contains" or "This text contains" but rather directly go to the conclusion.
If there is nothing really relevant, just say so. Do not invent anything, and explain what is missing and what you'd like to see.

# Example of answer

## Example 1
* "Economic", "Time Horizon", "5 years"
* Expected economic results of the innovation are indicated between 3 to 7 years.

# Now is your time to work! The text is as below:

"""
    )

    return background


def getWorkbook(CERNA_review,txt):
    book = openpyxl.load_workbook("template.xlsx")
    F, A = flavors, list(angles.keys())
    ws = book["review"]

    chars = "ABCDEFGH"
    for k in range(len(F)):
        for j in range(len(A)):
            print(F[k], A[j], chars[k], j)
            ws[chars[k + 1] + str(2*j + 3)] = CERNA_review[F[k]][A[j]].split("\n")[-1].strip("*").strip()
            ws[chars[k + 1] + str(2*j + 2)] = CERNA_review[F[k]][A[j]].split("\n")[0].strip("*").strip()
    if 0:
        for k in range(len(F)):
            ws[chars[k + 1] + "1"] = flavors[k]
        for j in range(len(A)):
            ws["A" + str(j + 2)] = A[j]
    ws = book["review"]
    ws["A1"] = txt
    return book