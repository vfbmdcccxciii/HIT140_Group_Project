# Three-minute discussion: Maximus Turner

Draft for rehearsal and adaptation. Speak slides 1-4 only. Keep your face visible throughout. At the start, show your CDU student ID to the camera for approximately five seconds. Do not read the bracketed directions aloud. Aim to finish by 2:55 to leave a margin within the three-minute limit. Review AI-use requirements in docs/ai_acknowledgement.md before using the wording.

## Slide 1: 0:00-0:40, including ID

[Show CDU student ID, then begin.]

I'm Maximus Turner. My two questions compare midfielders and forwards: how far they run per ninety minutes, and what share of their defensive pressures directly challenges the ball carrier.

The analysis joins FIFA player tables using player, team and position. A source check recovered 281 missing minutes records. Missing statistics stayed missing. Python performs the preparation, sampling, calculations and charts. For both questions, the null hypothesis is equal group means, tested against a two-sided alternative at five percent significance.

## Slide 2: 0:40-1:25

For running, players needed at least 180 minutes and recorded distance. Distance divided by minutes, multiplied by ninety, makes playing duration comparable. The random samples contain thirty players per position, using fixed seeds.

Midfielders averaged 9.74 kilometres per ninety, compared with 9.22 for forwards. The chart shows each mean and its ninety-five percent confidence interval. The estimated difference is 0.52 kilometres, with a difference interval from 0.22 to 0.82.

The course two-sample test gives t equal to 3.59, with 29 degrees of freedom, and p equal to 0.0012. We reject the null hypothesis.

## Slide 3: 1:25-2:15

The less obvious question concerns pressing composition. For each player, direct pressures divided by all pressures, multiplied by one hundred, gives a percentage. It describes pressing style, not success.

Players needed at least ninety minutes and positive recorded pressures. Forty players were sampled per position. Midfielders averaged 17.08 percent, compared with 11.20 percent for forwards. The difference is 5.88 percentage points, with a ninety-five percent interval from 2.14 to 9.63.

The test gives t equal to 3.18, with 39 degrees of freedom, and p equal to 0.0029. Again, we reject the null.

## Slide 4: 2:15-2:55

These findings are exploratory. The second question was selected after inspecting alternatives. Partial source coverage limits generalisation, and shared team tactics may weaken independence. Pressing is right-skewed, and plausible outliers were retained. Larger samples help, but do not remove these limitations.

My main lessons are that incomplete joins change the sample, denominators change a question's meaning, and a small p-value needs context. These samples suggest midfielders run farther and apply a larger share of pressures directly. They do not establish that playing position causes either difference.

[If another presenter follows, replace the final sentence or shorten the conclusion to add: "I'll now hand over for the next analysis." Keep total time under three minutes.]
