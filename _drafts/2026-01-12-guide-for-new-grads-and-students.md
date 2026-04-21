---
title: "Landing Your First Role"
date: 2026-01-12
categories:
  - reflections
tags:
  - career
  - advice
---

The junior tech market is hard. Companies hire fewer entry-level engineers. AI has made everyone's application look the same — candidates feed identical job descriptions into the same prompts, and recruiters see a thousand clones. For most people, resumes no longer tell them apart: incompetent, average, and competent candidates all look competent.

Hiring managers look for specific skills and qualities. Your goal — from resume to final interview — is to identify what they want and show you have it.

Securing a job is two steps: get the interview, then pass the interview. Both require working backward from the job description — extract the technical and behavioral signals the employer values (distributed systems, AWS, Python, C++), and let those drive what you emphasize in your interactions.

The easiest path is converting an internship into a full-time offer. If you have that option, take it.

**TL;DR:**
- **Get the interview:** tailor your resume to the job description with specific evidence, not keyword stuffing. Get a referral before you apply, not after.
- **Pass the interview:** ask clarifying questions, talk through your reasoning as you code, test your own code, and be fluent in one language.
- **Prepare three to five behavioral stories** that show problem-solving, disagreement, and ambiguity. Use "I," not "we."
- **Don't let LLMs trick you into feeling competent.** Reading their code isn't the same as writing your own.

## Getting the Interview

Your resume is a marketing document. Its purpose is to signal — within ten seconds of skimming — that you're the candidate the recruiter is looking for and that you're worth a senior engineer's time.

I'd recommend keeping it to one page. A recruiter processing a thousand applications spends fewer than fifteen seconds on each. They scan for university, standout projects, relevant experience, and recognizable company names. Your resume should catch their eye in that window, or it lands in the rejection pile.

Read the job description before you tailor your resume, especially for roles you want. If the posting asks for experience with React, TypeScript, and cloud infrastructure, your resume should reflect those skills — with specific evidence, not just keyword stuffing. Real project names, real outcomes, real tools. "Built a real-time dashboard using React and WebSockets that reduced incident response time by 40%" beats "proficient in JavaScript frameworks." Specific claims are believable. Vague ones aren't.

Don't over-focus on GPA. Unless you're aiming for a PhD or grad school, time spent chasing a perfect transcript yields diminishing returns. A 3.5 GPA with two shipped side projects and an open source contribution paints a better picture than a 4.0 with nothing else. Interviewers want evidence you can build things and contribute quickly, not that you can pass exams.

It's easy to tunnel-vision on coursework and miss how much real-world experience matters. Andrej Karpathy's [advice page](https://cs.stanford.edu/people/karpathy/advice.html) is worth reading on this.

Referrals matter, and not all referrals carry equal weight. In my experience, companies treat them in tiers:

- **Stranger referral:** "I don't know this person, but here's their resume." Better than a cold application.
- **Acquaintance referral:** "I know this person." Generally moves you past the initial screen.
- **Strong referral:** "I can vouch for this person's ability." This is the one that changes outcomes.

A strong referral from someone who can speak to your technical ability puts you in a different stage of the pipeline than a stranger clicking "refer" on LinkedIn. But even a stranger referral beats a cold application — don't be afraid to ask. Most people remember being in your position, and companies typically offer referral bonuses, so they have some incentive to help.

Timing matters on both sides. A referral submitted *after* you've already applied often does nothing — you're already in the system with a status, sometimes already rejected. Get the referral in before the application, not as a follow-up.

Same logic for the application itself: apply fast when a posting goes live. Companies post roles when they actually need someone, and the first suitable candidates through the door often get the interview.

Cold outreach works when you lead with genuine interest. Don't open with "can you refer me?" — that puts them in an awkward spot. Open with interest in the problem their team solves. Ask a specific question about their work. Both sides know you want a referral; the conversation should still be interesting.

## The LLM Trap: The Illusion of Competence

Using LLMs for learning creates a dangerous illusion. You prompt a model. It outputs an elegant solution. You read it and nod. You feel like you've learned.

You haven't.

Reading code is passive. Writing code is active. They are different cognitive processes. You can't outsource thinking to an LLM. I think this is the single biggest trap for people preparing for interviews, and for learning generally.

> "Writing is nature's way of letting you know how sloppy your thinking is." — Leslie Lamport (quoting Richard Guindon)

The test is simple: can you write the solution from scratch, on a whiteboard, with no autocomplete? Can you explain the importance of every line? Can you discuss the tradeoffs — why this approach over that one, what breaks if you remove this condition? If not, you have a surface-level understanding that will collapse under interview pressure.

[Anthropic found](https://www.anthropic.com/research/AI-assistance-coding-skills) that developers who used AI to generate code scored lower on comprehension than those who coded by hand — but those who used AI to ask questions and probe concepts didn't. How you use the tool determines whether it helps or harms you.

Used right, LLMs can make you think more, not less. Treat them as thinking partners, not answer machines. Tell the model to act as your interviewer. Give it context about the role you're preparing for. Ask it to evaluate your code without writing the solution. Ask it to give minimal hints, framed as questions, when you're stuck. When you get the answer right, ask it to hit you with a hard follow-up. The point is to use the tool in a way that forces you to think, not in a way that lets you skip thinking.

Another practical tip: practice in environments without autocomplete. Open a plain text editor, or even Microsoft Word, and solve problems there. Your interview environment won't have claude code and auto-complete.

One more practical tip: start fresh chat windows when conversations get long. If you keep getting wrong answers, start over.

## Passing the Interview

Not every company runs this full process — startups often compress it to a call, a take-home, and a handshake — but the core ideas apply.

Here's my read on the interviewer's side. Interviewers collect signals — positive and negative — throughout every interaction with you. At the end, they assign a score, ranging from strong no hire, no hire, leaning no hire, leaning hire, hire, to strong hire. That score reflects the signals you give them.

Your goal throughout every interaction: maximize positive signals, eliminate negative ones.

Eliminating negatives matters more than you'd expect. At larger companies, a hiring committee or debrief reviews all the interviewers' scores before making a decision. A single strong "no hire" from any round can override three "hire"s. Negative signals are asymmetrically expensive — so eliminating them is often worth more than chasing extra positives.

### The Recruiter Phone Screen

Between the application and the technical rounds sits the recruiter phone screen. These vary — sometimes it's a quick idiot check ("can you write code, are you still interested, where are you based?"), sometimes it's a real gatekeeping call where communication, enthusiasm, and fit are all being evaluated. You won't always know which one you're in, so treat every call as the gatekeeping version.

Recruiters are mostly on your side. They're measured on the hires they close, so their incentive is to get you signed — though not always at the highest salary. Anything that strengthens your profile — competing offers, active late-stage processes elsewhere, changes in your timeline — is worth telling them. They can use it to fight for you internally.

- **Know your resume.** They will ask about projects or experience you listed. Vague answers about your own work raise questions.
- **Have a specific "why this company" answer.** "I like your product" is generic. Referencing a particular team, product decision, or engineering blog post shows you've done the research.
- **State your timeline honestly.** If you have other processes moving or competing offers, say so. That gives the recruiter something to work with on your behalf.
- **Be careful with compensation numbers.** If they ask, give a wide range with the bottom end at or above what you'd actually accept. The numbers you state anchor the negotiation, so aim high.

### Technical Interview

It helps to think backward. If you know their marking criteria, you can prepare for exactly what they're evaluating. From my understanding, interviewers score you along four dimensions: algorithms, communication, problem solving, and coding ability. Every action you take in the interview room either strengthens or weakens one of these scores.

**Be friendly and pleasant to work with.** Interviewers are evaluating whether they want to work with you eight hours a day. Borderline technical performances can swing on likability — "leaning hire" becomes "hire" when the candidate is pleasant to work with, and the reverse happens too. Arrogance, dismissiveness, and arguing with the interviewer's suggestions are instant red flags. Strong technical skill rarely compensates for a personality nobody wants on their team.

**Ask clarifying questions before you code.** Most interview problems are deliberately ambiguous — interviewers omit constraints on purpose and leave edge cases undefined. Jumping straight into code tells the interviewer you don't think before you build. Interviewers score accordingly.

**Communicate your thinking as you work.** Talk through your approach before you code. Think out loud as you implement. I know this is unnatural — nobody talks while they code in real life — so practice it until it feels less strange. Silent coding is a black box: the interviewer can only evaluate the final output, and if it's wrong, they have no partial credit to give.

**Test your code without being asked.** Choose your own inputs, state the expected output, and trace through line by line. Demonstrating it unprompted shows the interviewer you take correctness seriously. Skipping it signals the opposite — and that's a concern interviewers carry into their scoring.

**Understand the tradeoffs of your solution.** When you finish, explain why you chose this approach over alternatives. Discuss time and space complexity without being asked. If your solution has a known ceiling, name what you'd try with more time. It tells the interviewer you aren't just pattern-matching from a problem set, but reasoning about the solution.

**Follow the interviewer's lead.** If they nudge you in a direction, follow it — they've prepared questions along that path. If they hint that your approach has a flaw, don't defend it; reconsider it. If they ask a direct question, answer it directly. If they mention time, take the hint. Interviewers read this as coachability — a quality every team values.

**Be honest about what you don't know.** "I don't know, but let me think through it" earns far more respect than a confident answer that falls apart under follow-up questions. A few honest "I don't know"s are generally neutral. Faking knowledge is worse. The moment the interviewer catches one bluff, they question everything else you said. The interviewer will probe anything on your resume. Don't put it there unless you can defend it.

**Know your language well.** If you can't create a hashmap or check whether a key exists in your language of choice, that's a severe negative signal — it suggests you don't write code regularly. Same with repeated syntax errors: forgetting semicolons, misusing brackets, confusing method names. Minor slip-ups from nerves are fine, especially if you catch and correct them. A pattern of them is not. Pick one language and know it well.

**Stay calm on hard problems.** Leetcode hards in interviews are rare. Quant firms may differ, but at most companies, if you get a hard problem, the interviewer doesn't expect you to breeze through it. They want to see your process, your thinking, and how you handle difficulty. Staying calm and methodical on a problem you can't fully solve is a strong signal in itself.

**Ask insightful questions at the end.** Every interview closes with "do you have questions for me?" Asking nothing signals disinterest. Ask something that shows you've thought about the company, the team, or the problem space. This is also your chance to evaluate whether you'd actually want to work there.

### Behavioral Interview

Behaviorals matter as much as technical interviews, and they matter more as you grow senior. Two things get tested: whether your experience aligns with the kind of candidate they need, and whether the claims on your resume hold up when you're asked to walk through them.

Prepare stories in advance using STAR or a similar structured frame — context, problem, your approach and tradeoffs, impact. Three to five stories from school, internships, or projects will cover most of what gets asked: a time you solved a hard technical problem, a time you handled a disagreement, a time you dealt with ambiguity or failure. Practice telling them out loud. They should run two to three minutes, not ten, and the focus should be on "I," not "we."

Larger companies also screen for cultural fit against a specific list of values they publish — Amazon's Leadership Principles, Canva's "Crazy Big Goals," Google's "Googleyness." The interviewer has a list of questions, and each question usually maps to one of those values. Before you answer, take a moment to identify which attribute the question is getting at, then pick the story that best shows it. Researching the company's stated values ahead of time makes this easier.

## After the Interview

Ask for feedback when you get rejected. Recruiters usually aren't allowed to give detailed feedback — legal reasons — but some will drop hints if you ask politely. *"Is there anything specific I should work on?"* or *"Was this close, or should I focus elsewhere?"* Even a vague answer tells you where to look — resume, technical prep, or behaviorals.

Also keep your own notes. After each interview, write down the questions you got, what you answered well, what you bombed. Patterns emerge across interviews, and they usually tell you what to fix: if you're getting cut at the resume stage, fix the resume; at the first technical, fix your algorithms; at behavioral rounds, fix your stories.

If something isn't working, change it. If your resume isn't landing interviews, fix the resume — don't send the same one to 200 more companies.

## Resources

Recruiter-provided preparation materials are the most important resource — study them first. They often hint what you'll be tested on. Beyond that: [Neetcode](https://neetcode.io/) for leetcode preparation, and [A Life Engineered](https://www.youtube.com/@ALifeEngineered) (Steve) on YouTube for broader career perspective.

## Closing

Don't put too much hope in any single company. Accept rejections and keep going.

Sometimes the rejection isn't about you. Companies post roles during hiring freezes, fill them internally, or lose budget mid-process. You'll rarely know for sure.

Good luck! :)
