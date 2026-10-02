import json,os
os.chdir('/data/why-we-become-everyone-else-living-better');exec(open('build_timeline.py').read().split('# ---------- sheets / panels ----------')[0])
ls=[{'text':t,'start':line_start[k]} for k,(i,t) in enumerate(say)];snap=lambda t:min(ls,key=lambda l:abs(l['start']-t))['start'];sc=[]
DATA='''0;01-1;timeline;A normal day.;YOUR LIFE|NORMAL;0,1.3
3.7;01-2;feed;Then you open / your phone.;OPEN|SCROLL;3.7,4.1
5.4;01-3;meter;Nothing changed. / Except the feeling.;ACTUAL LIFE|HOW IT FEELS;8.1,5.4;dark
14.9;01-4;feed;Their highlights.;TRAVEL|NEW CAR|BUSINESS|MARRIAGE;14.9,16.5,17.8,19
20.2;01-5;stack;A bigger feed. / A smaller feeling.;ANOTHER COUNTRY|SAME AGE|YOUR DREAM;20.2,22.1,25.2
28.3;01-6;thought;The questions / start.;WHY NOT ME?|WHAT AM I DOING?;29.5,30.8
32.3;01-7;paths;Moving forward. / Falling behind?;EVERYONE ELSE|ME;32.3,34
35.9;01-9;split;Looks better. / Is better?;APPEARANCE|REALITY;41.2,43.4
45.7;01-8;window;A tiny window. / Your whole story.;THEIR HIGHLIGHT|YOUR WHOLE LIFE;48.5,51;dark
53.6;01-9;focus;Change the / reference point.;NOTICE COMPARISON|SEE IT DIFFERENTLY;53.6,55.9
58.6;02-1;feed;The highlight reel.;INSTAGRAM|YOUTUBE|TIKTOK;58.6,60.5,61.5
64.6;02-2;feed;One post / after another.;TRAVEL|MONEY|FITNESS;64.6,66.3,68
69.5;02-3;stack;All the best parts.;COMPANY|APARTMENT|FRIENDS|CONFIDENCE;69.5,71,74.7,77.7
79.6;02-4;meter;Ten minutes. / A different mood.;DOZENS OF HIGHLIGHTS|ONE ORDINARY LIFE;80.9,83.3
84.5;02-6;stack;What stays / off-screen.;BORING TUESDAY|FAILED PLANS|UNCERTAINTY|LONELINESS|DOUBT;85.9,87.5,89.4,91.1,92.1
95.1;02-5;feed;Worth showing.;RESULT|PHOTOGRAPH|ANNOUNCEMENT|ACHIEVEMENT;95.1,95.9,96.9,98
99.1;02-7;window;Five seconds / of a whole life.;SELECTED MOMENT|EVERYTHING ELSE;99.1,101.1
102.8;02-8;split;The unseen / comparison.;PUBLIC HIGHLIGHT|PRIVATE REALITY;102.8,105.1
106.4;02-9;balance;Not a fair / comparison.;TINY HIGHLIGHT|ENTIRE LIFE;106.4,107.6;dark
109.3;03-1;network;An ancient / habit.;COMPARE|FIND YOUR PLACE;111.2,114.9
117.6;03-2;split;Who stands / above you?;STRONGER|MORE RESPECTED|MORE CAPABLE;119,120.5,123.3
124.5;03-3;network;Inside / a group.;SOCIAL POSITION|LOCAL GROUP;124.5,127.8
129.9;03-5;network;A small / comparison pool.;PEOPLE AROUND YOU|DOZENS|HUNDREDS;129.9,132.6,134.1
135.4;03-6;counter;Now: / millions.;MILLIONS|BEFORE BREAKFAST;135.8,137.5
140;03-7;stack;Every extreme. / All at once.;RICHEST|MOST SUCCESSFUL|MOST TALENTED|MOST ADVENTUROUS|MOST PRODUCTIVE;140,141.5,142.7,144,145.5
147.3;03-8;network;An overloaded / reference point.;FIVE MINUTES|UNUSUAL EXAMPLES;147.3,150.7
153.5;03-4;stairs;It feels / like everyone.;WHAT THE FEED SHOWS|WHAT YOUR BRAIN ASSUMES;153.5,155.4
157.8;03-9;focus;That is / the illusion.;SELECTION ≠ EVERYONE;157.8;dark
159.8;04-1;dots;A room / of 100.;100 PEOPLE;162
164.4;04-2;dots;95 ordinary / days.;95 ORDINARY|5 EXCITING;164.4,168.2
170.7;04-3;feed;Five exciting / moments.;PROMOTION|TRAVEL|BUSINESS|ENGAGEMENT;170.7,172.5,174.7,176.5
178;04-4;window;The camera / chooses.;100 IN THE ROOM|5 IN THE FRAME;178,180.2
182.6;04-5;focus;Watch only / the highlights.;SELECTED FOOTAGE|PERCEIVED REALITY;182.6,184.3
187.2;04-6;feed;Everyone looks / extraordinary.;THE FEED|THE IMPRESSION;187.2,188.4
190.6;04-7;split;Reality. / A selection of it.;WHOLE ROOM|SELECTED FIVE;190.6,193;dark
195.1;04-8;dots;The rest / stays invisible.;SEEN|NOT SHOWN;195.1,197.2
199.1;04-9;window;Worth showing. / Not the whole story.;CURATED MOMENTS;199.8
202;05-4;paths;Not random / comparisons.;YOUR INSECURITY|YOUR ATTENTION;203.5,208.6
211.3;05-1;meter;Worried / about money?;MONEY WORRY|NOTICE MORE MONEY;211.3,212.9
215.3;05-2;stairs;Worried about / your career?;CAREER WORRY|NOTICE PROMOTIONS;215.3,216.9
218.7;05-3;split;Worried about / your social life?;FEEL ALONE|NOTICE FRIEND GROUPS;218.7,220.9
223.1;05-8;paths;Worried about / your future?;YOUR QUESTIONS|THEIR CERTAINTY;223.1,224.9
227.7;05-5;search;A search engine / for being behind.;EVIDENCE I AM BEHIND|MORE RESULTS;229.5,232.8
233.9;05-6;focus;How do / I measure up?;SEARCH|COMPARE|SEARCH AGAIN;233.9,240.6,241.9
243.6;05-7;stairs;Someone is / always ahead.;YOUNGER|RICHER|MORE EXPERIENCED|MORE TALENTED|EARLIER START;245.7,246.7,247.6,249.2,250.6
256.3;05-8;meter;Your achievement / still counts.;YOUR GOAL|SOMEONE ELSE’S GOAL;256.3,260.3
263.2;05-9;finish;The finish line / keeps moving.;ACHIEVE|COMPARE|MOVE THE GOAL;263.2,264.3,265.9;dark
267.9;06-1;loop;Achievement / becomes a loop.;GET THE JOB|WANT A BETTER JOB|FEEL BEHIND|CHASE AGAIN;267.9,269.1,271.6,278.5
270.5;06-3;loop;Progress / meets comparison.;REACH A GOAL|SOMEONE WAS FASTER|FEEL BEHIND|CHASE AGAIN;270.5,271.6,277.2,278.5
273.8;06-4;feed;Better than / what you have.;WANTED IT|GOT IT|SAW SOMETHING BETTER;273.8,274.5,275.3
277.2;06-2;stairs;Further ahead. / Again.;YOUR PROGRESS|THE NEXT LEVEL;277.2,278.5
281;06-5;loop;A moving / scoreboard.;ACHIEVE|FIND SOMEONE AHEAD|FEEL BEHIND|CHASE A NEW GOAL;281,283.8,286.6,287.9;dark
289.9;07-5;split;Wanting it. / Or seeing it?;YOUR DESIRE|SOMEONE ELSE HAS IT;292.5,295.9
297.9;06-6;paths;Borrowed / desires.;THEIR TRAVEL|YOUR NEW WANT|THEIR BUSINESS|YOUR NEW PLAN;297.9,299.5,301.1,303
305.6;06-7;clock;Borrowed / routines.;05:00|GUILT FOR SLEEPING;305.6,307.9
310.1;06-8;counter;Someone else’s / reading pace.;50 BOOKS|YOUR OWN PACE;310.1,312.3
315.7;06-9;thought;Questioning / your own future.;THEIR CERTAINTY|YOUR DOUBT;315.7,319.6
321.6;07-4;thought;If nobody / could see it…;WOULD YOU STILL WANT IT?;325.1;dark
328.8;07-3;split;A better life. / Or a better look?;FEELS BETTER|LOOKS BETTER;329.7,333
337.1;07-1;switch;Remove / the audience.;VISIBLE|PRIVATE;337.1,338.4
340.6;07-2;counter;No audience. / Still your life.;FOLLOWERS|LIKES|PEOPLE TO IMPRESS;341.7,342.4,343
344.1;07-3;feed;No one / would know.;MONEY|CAR|TRAVEL|PRODUCTIVITY|ACHIEVEMENTS;344.1,346.1,348.1,349.8,352
353.9;07-9;paths;What would / you choose?;YOUR LIFE|YOUR CHOICE;353.9,356.9
361.4;07-6;thought;Do these / goals fit you?;YOUR GOALS?|BORROWED GOALS;363.7,366.9
368.2;07-7;focus;Ambition is / not the problem.;SUCCESS|MONEY|A BETTER LIFE;368.2,370.4,374.1
375.5;07-8;paths;Who decides / your direction?;THEIR LIFE|YOUR LIFE;375.5,378.1;dark
381.6;08-1;iceberg;The missing / context.;CURRENT POSITION|STARTING POINT;385.5,383.7
387.2;08-2;paths;Different / starting lines.;OPPORTUNITIES|DIFFERENT STARTS;387.2,388
389.2;08-3;stairs;The help / you didn’t see.;SUPPORT|CONNECTIONS|HELP;389.2,389.5,390
390.5;08-4;meter;The sacrifices / you don’t know.;VISIBLE RESULT|INVISIBLE COST;390.5,392.2
394.1;08-5;window;The unseen / work.;BEHIND THE SCENES|YEARS OF PRACTICE;394.1,396.2
399.8;08-6;split;Looks successful. / Feels fulfilled?;OUTSIDE|INSIDE;402.6,405.4
407.8;08-7;thought;Not enough / information.;MISSING CONTEXT|YOUR BRAIN ADDS A STORY;407.8,410.1
415;08-8;loop;The story / repeats.;THEY’RE DOING BETTER|I’M BEHIND|THEY FIGURED IT OUT|I HAVEN’T;415,416.2,417.2,418.5
421.3;08-9;thought;Repeated. / Not proven.;REPETITION|BELIEF;421.3,423.5;dark
428;09-1;meter;The cost / of comparing.;PROGRESS|CONSTANT MEASURING;433.4,435
436.7;09-2;paths;You stop / your own work.;YOUR GOAL|THEIR POSITION;436.7,438.2
439.9;09-3;window;You look away / from your own life.;YOUR LIFE|SOMEONE ELSE’S LIFE;439.9,441.6
444.2;09-4;focus;You abandon / what mattered.;GENUINE INTEREST|NOT IMPRESSIVE ENOUGH;445.3,447.9
450.4;09-5;split;Two learners. / Same skill.;LEARNER A|LEARNER B;450.4,452.5
452.5;09-6;stairs;Enjoying / the process.;SLOW IMPROVEMENT|ENJOY THE PROCESS;452.5,454.3
455.8;09-7;feed;Checking / everyone else.;SAME SLOW IMPROVEMENT|COMPARE THE FEED;455.8,457.7
460.2;09-8;split;Same progress. / Different experience.;I’M GETTING BETTER|I’M STILL BEHIND;464.2,466.5
467.7;09-9;balance;A different / scoreboard.;ME VS PAST ME|ME VS EVERYONE;467.7,470.1;dark
471.7;10-1;thought;Notice the / comparison.;NOT DELETE EVERYTHING|NOT STOP CARING|NOTICE CONTROL;473,475.7,485.4
489.1;01-6;thought;Behind / according to who?;I’M BEHIND|PAUSE|ACCORDING TO WHO?;491.8,492.7,494.5;dark
498.6;10-2;paths;Not the / same timeline.;THEIR TIMELINE|YOUR TIMELINE;500.8,503.9
506.9;07-9;paths;A different path. / Not a wrong one.;NOT BEHIND|YOUR OWN PATH;508.1,509.6
511.4;10-3;split;Better than / you were.;BETTER THAN THEM?|BETTER THAN I WAS?;515,517.2
520.9;10-3;timeline;Your past self. / Your reference.;PAST YOU|PRESENT YOU;522,523
524.4;10-4;stack;Real progress.;LEARNED|DISCIPLINE|HARD DECISION|SELF-UNDERSTANDING|KEPT GOING;524.4,525.7,527.6,531,533
535.3;10-5;iceberg;Invisible / progress.;NOT IMPRESSIVE ONLINE|STILL REAL;535.3,537.6
542.8;10-6;stack;The work / nobody sees.;CHOOSING WELL|PRACTICING|STUDYING TIRED|KEEPING A PROMISE;542.8,545.5,548.4,550.6
553.5;10-5;stairs;Small decisions. / Real change.;SMALL CHOICES|STILL COUNT;553.5,556.9
558.6;10-7;switch;Your life is / not a performance.;AUDIENCE|YOUR LIFE;558.6,560.5
565;10-8;stairs;Build a life / that feels like yours.;YOUR GOALS|YOUR DIRECTION|YOUR LIFE;570.7,575.8,578.2
582;07-4;thought;Change / the question.;WHAT LIFE DO I WANT?;588;dark
590.4;10-2;paths;The next step. / Not their step.;WHY SO FAR BEHIND?|WHAT’S NEXT FOR ME?;591.3,593.3
594.8;07-5;split;Do I even / want that?;WHAT THEY HAVE|WHAT I WANT;595.5,597.9
599.3;10-3;timeline;Someone / you respect.;AM I WINNING?|AM I BECOMING?;600.1,601.8
603.7;10-9;focus;Look at / your own life.;EVERYONE ELSE|YOUR OWN LIFE;608.3,610.5
612.3;01-2;feed;Remember / the window.;OPEN PHONE|NOTICE THE FEELING;612.3,613.6
616;02-8;split;Highlight ≠ life. / Outcome ≠ process.;HIGHLIGHT / WHOLE LIFE|OUTCOME / PROCESS|SELECTED / EVERYTHING;616,618.5,621
624.2;01-8;window;A tiny window. / An unfair comparison.;THEIR WINDOW|YOUR WHOLE STORY;624.2,625.5
629.9;01-1;timeline;Keep your / ordinary Tuesday.;AN ORDINARY DAY|STILL YOUR LIFE;631.8,633.2
634.4;10-2;paths;Their timeline / is not your rule.;THEIR TIMELINE|YOUR TIMELINE;634.4,635.8
637.5;09-9;split;Their success / is not your failure.;THEIR SUCCESS|YOUR LIFE;637.5,639.4;dark
641.3;10-8;stairs;Build / your own.;YOUR OWN LIFE|THAT’S ENOUGH;642.9,645.5
646;10-9;focus;Why We Become.;THINK DEEPER|LIVE BETTER|BECOME MORE;646,646.8,647.9'''
CH=[0,58.58,109.31,159.77,201.96,267.865,337.105,381.595,428.01,471.7,511.4,565]
for row in DATA.splitlines():
 a=row.split(';');t,art,kind,title,lab,cues=a[:6];start=snap(float(t));dark='dark' in a[6:];sc.append(dict(start=start,art=art,kind=kind,title=title.replace(' / ','\n'),labels=lab.split('|'),cues=[snap(float(x)) for x in cues.split(',')],dark=dark))
for i,s in enumerate(sc):
 s.update(id=i,end=sc[i+1]['start'] if i+1<len(sc) else words[-1]['end'],layout='right' if i%3==0 else 'left',chapter=max(j+1 for j,t in enumerate(CH) if s['start']>=t-.03))
 s['feature']=s['kind'] in ('dots','counter') or (s['dark'] and s['kind'] in ('loop','thought','focus','balance'));s['phrase']=min(ls,key=lambda l:abs(l['start']-s['start']))['text'];s['cues']=[max(s['start'],x) if x<s['end']-.08 else s['end']+1 for x in s['cues']]
assert len({s['art'] for s in sc})==90
json.dump(sc,open('v2/scene_plan.json','w'),indent=1);open('v2/panel_sync_review.md','w').write('# Panel / audio edit map\n\n'+'\n'.join(f"- {s['start']:.3f}–{s['end']:.3f}s · {s['art']} · {s['phrase']} → {s['kind']}" for s in sc))
s=open('subs.ass').read().replace('ExtraBold,72,','ExtraBold,60,').replace('1,5.5,2,2,100,100,90,1','1,4.0,1.5,2,100,100,82,1');open('v2/captions.ass','w').write(s)
seo=open('seo.md').read().replace('## Chapters (timestamps to be finalised after render)','## Chapters')
for i,t in enumerate(CH[1:],2):m,se=divmod(int(t),60);seo=seo.replace(f'[{i:02d}]',f'{m:02d}:{se:02d}')
open('v2/seo.md','w').write(seo);print(len(sc),'scenes, 90 panels')
