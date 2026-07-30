# 🧊 Cold Data Storage Medium — Market Research & Partner Feedback
**Last Updated:** 2026-07-26T02:18:26.381018

---

## 📌 1. Capacity & Supply Pressures
*Capacity expansion, energy constraints, and market supply shortages*

> **Quote #1:** “Our datacenter power budgets are capped at 50MW per site. If a cold storage solution can't halve the Watts per petabyte, we literally can't plug in more racks regardless of drive density.”
> 
> — **Speaker:** VP of Infrastructure, Top-5 Cloud Provider
> — **Key Takeaway:** Energy cap is the primary hard bottleneck over raw physical space.
> — **Source File:** `call_notes_2026_07_15_cloud_arch.txt` (2026-07-15)

> **Quote #2:** “Hyperscalers are now placing non-cancellable purchase orders for drives that won't be manufactured until sometime in 2028, some of them 2029. This is literally sucking the life out of the supply chain for anybody below a Hyperscaler or the largest server manufacturers like Dell and HP.”
> 
> — **Speaker:** Michael Hardy, VP Alliances & OEM, Quantum Corp
> — **Key Takeaway:** Hyperscalers locking in non-cancellable HDD purchase orders 3-4 years out (2028-2029), drying up supply for non-hyperscalers.
> — **Source File:** `GLG_Interview_Michael_Hardy_Quantum_2026_07_17.pdf` (2026-07-26)

> **Quote #3:** “The cost of flash drives has gone up literally 5x in the last six months. So there's a big push to really focus as an end user, what exactly needs to be on flash and what doesn't need to be on flash? ... We're all constrained on the number of drives we get out of IBM, because IBM is the sole manufacturer of LTO tape drives and everybody on the planet is on allocation out of IBM.”
> 
> — **Speaker:** Michael Hardy, VP Alliances & OEM, Quantum Corp
> — **Key Takeaway:** Flash costs surged 5x in six months; IBM single-source monopoly on LTO tape drives leaves all buyers on tight allocation.
> — **Source File:** `GLG_Interview_Michael_Hardy_Quantum_2026_07_17.pdf` (2026-07-26)

> **Quote #4:** “The indications we're getting out of Hyperscale are that there is no end to the amount of data that's being generated and they're being asked to store and they can't even buy disk. Like I said, they have orders out that won't be fulfilled for two years and they can't buy enough tape drives today, they can't buy enough tape media today.”
> 
> — **Speaker:** Michael Hardy, VP Alliances & OEM, Quantum Corp
> — **Key Takeaway:** Endless storage expansion demand colliding with multi-year manufacturing lead times for both magnetic disk and tape media.
> — **Source File:** `GLG_Interview_Michael_Hardy_Quantum_2026_07_17.pdf` (2026-07-26)

> **Quote #5:** “The shortage of HDDs was caused by a sudden demand spike due to a strong constraint in SSD supply... Western Digital and Seagate announced that all the capacity that they are able to build through 2027, it has been already committed... So that means the shortage of the HDD is going to be remaining beyond 2027. We are looking even to 2028.”
> 
> — **Speaker:** Dinesh Kumar, Former Procurement & Supply Chain Lead, Meta & AWS
> — **Key Takeaway:** Western Digital & Seagate drive manufacturing capacity completely sold out through 2027; supply pinch extended into 2028.
> — **Source File:** `GLG_Interview_Dinesh_Kumar_Meta_AWS_2026_07_21.pdf` (2026-07-26)

> **Quote #6:** “This demand and supply cycle is not superficial. That means from the supplier point of view, they are really in a very tight situation that they cannot meet the demand and that their capacity to build is already committed through next 18-20 months... It is really driven by the demand that Hyperscalers are putting on the hard drives.”
> 
> — **Speaker:** Dinesh Kumar, Former Procurement & Supply Chain Lead, Meta & AWS
> — **Key Takeaway:** Genuine non-superficial supply deficit backed by 18-20 month committed hyperscaler order books.
> — **Source File:** `GLG_Interview_Dinesh_Kumar_Meta_AWS_2026_07_21.pdf` (2026-07-26)

> **Quote #7:** “My estimation is that on a year over year basis, the demand for hard disk drive... is projected to be in the range of around 18-25%, maybe 18-22% year over year for the next five to seven years... If SSD supply fails to meet demand and prices remain significantly higher than HDD prices, hyperscalers might continue to use HDDs to avoid spending 2x to 5x more on SSDs.”
> 
> — **Speaker:** Dinesh Kumar, Former Procurement & Supply Chain Lead, Meta & AWS
> — **Key Takeaway:** 18-25% YoY baseline growth for HDDs over next 5-7 years; 2x-5x price premium on SSDs protects HDD volumes.
> — **Source File:** `GLG_Interview_Dinesh_Kumar_Meta_AWS_2026_07_21.pdf` (2026-07-26)


## 📌 2. Workloads & Data Tiering
*Partner data footprints from 'frozen' archival to 'hot' active tiers*

> **Quote #1:** “Over 80% of our sequencing archives are touched less than once every two years, yet compliance requires 30-year retention. Tape retrieve times kill automated bioinformatics jobs.”
> 
> — **Speaker:** Principal Data Architect, Genomics Research Institute
> — **Key Takeaway:** Frozen archival needs random-read access under hours, not days.
> — **Source File:** `interview_genomics_lab.txt` (2026-07-18)

> **Quote #2:** “I heard two days ago that the number is still probably 30X on primary tier versus the archival tier. The archival tier at some of these hyperscalers is measured in exabytes... If the world was smart and on the ball, then that ratio would flip completely. Because again, most data on the planet is cold or flat out trash. They call it ROT, redundant, obsolete, or trash. Most data, in fact, is that today. It's been this way since the '80s that roughly 70%-80% of the data, once it gets to 90-days-old, it's never going to be looked at again, period.”
> 
> — **Speaker:** Michael Hardy, VP Alliances & OEM, Quantum Corp
> — **Key Takeaway:** Primary storage holds 30x more volume despite 70-80% of post-90-day data never being accessed again ('ROT').
> — **Source File:** `GLG_Interview_Michael_Hardy_Quantum_2026_07_17.pdf` (2026-07-26)

> **Quote #3:** “They're generating more and more assets because AI is helping them do things. They're not wanting to delete data because they don't know the value of their data, because next year, a new model might come out that allows them to take advantage of this data. So it's impossible to value data anymore. So more data is being retained.”
> 
> — **Speaker:** Michael Hardy, VP Alliances & OEM, Quantum Corp
> — **Key Takeaway:** Future AI foundation model training potential makes valuing or deleting historical data nearly impossible.
> — **Source File:** `GLG_Interview_Michael_Hardy_Quantum_2026_07_17.pdf` (2026-07-26)

> **Quote #4:** “Archive is a write problem, not a read problem. By the time you've filled an archive, God, we've got statistics where massive archives are deployed on tape, where the tapes have only been mounted one time after writing, 96% of them, so this is a write problem. Writers need to be miniaturized.”
> 
> — **Speaker:** Michael Hardy, VP Alliances & OEM, Quantum Corp
> — **Key Takeaway:** 96% of cold archive cartridges are mounted only once after writing; high-throughput writing dominates access patterns.
> — **Source File:** `GLG_Interview_Michael_Hardy_Quantum_2026_07_17.pdf` (2026-07-26)

> **Quote #5:** “In 2026, Meta is planning to deploy approximately 2.5 gigawatt of compute capacity, and they require approximately 25 exabyte of storage... Between the three my understanding is the cold storage is going to be something around, I would say around 50%, the warm storage is going to be around 30% or 30-35%, and 15% is going to be hot storage.”
> 
> — **Speaker:** Dinesh Kumar, Former Procurement & Supply Chain Lead, Meta & AWS
> — **Key Takeaway:** At 25 Exabytes total scale, Meta's storage splits ~50% Cold archival, 35% Warm NAS, and 15% Hot flash.
> — **Source File:** `GLG_Interview_Dinesh_Kumar_Meta_AWS_2026_07_21.pdf` (2026-07-26)

> **Quote #6:** “Generally in the cold storage we are talking about several minutes. Best case... Cold storage is all dependent upon your application. Some data center might require access every few hours or every few minutes, but there are data centers which do not require access to the cold storage for several days or several weeks as well.”
> 
> — **Speaker:** Dinesh Kumar, Former Procurement & Supply Chain Lead, Meta & AWS
> — **Key Takeaway:** Cold storage retrieval SLA tolerance ranges from minutes best-case to days or weeks for non-critical archives.
> — **Source File:** `GLG_Interview_Dinesh_Kumar_Meta_AWS_2026_07_21.pdf` (2026-07-26)

> **Quote #7:** “The deployment of tapes is something that does not even come to my attention when I'm evaluating... Pure Storage has a partnership with Meta to build a cold storage capacity as one of their deliverables... In my knowledge, Pure Storage is not purchasing any tapes on behalf of Meta for those data centers. They are primarily purchasing hard disk drive as a main media.”
> 
> — **Speaker:** Dinesh Kumar, Former Procurement & Supply Chain Lead, Meta & AWS
> — **Key Takeaway:** Hyperscale social networks like Meta rely almost exclusively on high-density HDDs over physical tape libraries.
> — **Source File:** `GLG_Interview_Dinesh_Kumar_Meta_AWS_2026_07_21.pdf` (2026-07-26)


## 📌 3. Emerging Tech & Value Prop
*Appetite for novel storage mediums and required target metrics*

> **Quote #1:** “We would consider replacing optical or tape if a new medium demonstrated 50+ year write-once durability without requiring periodic media refreshing or magnetic decay migration.”
> 
> — **Speaker:** Head of Storage Engineering, Global Financial Institution
> — **Key Takeaway:** Zero-migration media lifetime (>50 yrs) is the killer feature.
> — **Source File:** `fintech_storage_lead.txt` (2026-07-20)

> **Quote #2:** “I wouldn't say optimistic. I'm freaking hopeful because magnetics is going to run out of gas someday. You can only get so small with the magnetic media and you can only get so much magnetic signal out of a small piece... Even with tape, we're running now in the nanometer scales to where at some point, magnetics just won't carry the day anymore.”
> 
> — **Speaker:** Michael Hardy, VP Alliances & OEM, Quantum Corp
> — **Key Takeaway:** Magnetic physics approaching hard nanometer physical scaling ceilings, opening a window for non-magnetic media.
> — **Source File:** `GLG_Interview_Michael_Hardy_Quantum_2026_07_17.pdf` (2026-07-26)

> **Quote #3:** “The hard part is miniaturization of the writer and the cost of the laser... The lasers themselves are really, really expensive and you need one really, really expensive laser per writer. You need at least 10 writers inside a rack with a bunch of storage around it to get to the areal densities relative to floor space to make this a viable technology.”
> 
> — **Speaker:** Michael Hardy, VP Alliances & OEM, Quantum Corp
> — **Key Takeaway:** Glass/optical commercial viability depends on laser cost scaling and mechanical multi-writer miniaturization.
> — **Source File:** `GLG_Interview_Michael_Hardy_Quantum_2026_07_17.pdf` (2026-07-26)

> **Quote #4:** “Tape is constrained at 400 megabytes per second and there's probably not going to be a lot of improvement in the speed of tape because we've about run out of room on bit density... at this point, any large tape user is starting to complain about the ratio between capacity and performance.”
> 
> — **Speaker:** Michael Hardy, VP Alliances & OEM, Quantum Corp
> — **Key Takeaway:** 400 MB/s per-tape-drive write throughput ceiling leaves enterprise users complaining about capacity-to-bandwidth ratio.
> — **Source File:** `GLG_Interview_Michael_Hardy_Quantum_2026_07_17.pdf` (2026-07-26)

> **Quote #5:** “Yes, so there is definitely a strong desire to use some of these advanced thermal coefficient material, polycarbonate, optic glass fiber, high-grade metal parts... Silica... Ceramic... The idea behind using these advanced materials is to improve the thermal loss, improve the dielectric constant, and making sure that these hard drives are operating in the most optimum temperature.”
> 
> — **Speaker:** Dinesh Kumar, Former Procurement & Supply Chain Lead, Meta & AWS
> — **Key Takeaway:** Strong buyer desire for ceramic, glass fiber, silica, and high-grade metal parts to manage thermal performance.
> — **Source File:** `GLG_Interview_Dinesh_Kumar_Meta_AWS_2026_07_21.pdf` (2026-07-26)

> **Quote #6:** “The reality is if you think about the data center like Meta, generally we have to do a major hard drive replacement cycle every 3-5 years. And if we are able to extend that to 7-10 years without requiring any major operational cost... or maybe 15 years, 20 years, this way I can look at a lower operational and lower replacement cost.”
> 
> — **Speaker:** Dinesh Kumar, Former Procurement & Supply Chain Lead, Meta & AWS
> — **Key Takeaway:** Replacing 3-5 year HDD refresh cycles with 10-20 year long-lived media delivers game-changing TCO reductions.
> — **Source File:** `GLG_Interview_Dinesh_Kumar_Meta_AWS_2026_07_21.pdf` (2026-07-26)

> **Quote #7:** “Assume for a minute that a cold storage hard drive of 256 terabytes consuming 10 milliwatts per second... Now, if hard drive vendor is able to bring that down to one milliwatt per second, that can be a significant gain in our total power budget... When we talk about in the context of 20 exabytes, 30 exabytes... that can be several tens of megawatts of saving.”
> 
> — **Speaker:** Dinesh Kumar, Former Procurement & Supply Chain Lead, Meta & AWS
> — **Key Takeaway:** Cutting idle drive draw from 10 mW/sec to 1 mW/sec frees up tens of megawatts at exabyte scale.
> — **Source File:** `GLG_Interview_Dinesh_Kumar_Meta_AWS_2026_07_21.pdf` (2026-07-26)


## 📌 4. Performance & Buying Criteria
*Top purchasing metrics: TCO ($/TB), Durability, Power, and Restore Speed*

> **Quote #1:** “At archival scale, dollar-per-terabyte cap-ex is only half the formula. If ingress/egress fees or media translation hardware cost more than $3/TB upfront, procuring procurement won't approve.”
> 
> — **Speaker:** Director of Platform Ops, Enterprise SaaS Provider
> — **Key Takeaway:** Total acquisition cost under $3/TB loaded is critical benchmark.
> — **Source File:** `saas_platform_call.txt` (2026-07-22)

> **Quote #2:** “Write speed dictates how much you can ingest and you take how much you can ingest or how much you need to ingest divided by how much you can ingest based on your investment. Write speed's always going to be a primary driver... Then at the top, what is my total cost of ownership versus my alternatives?... I would probably put at the bottom time to data as long as it's not measured in hours.”
> 
> — **Speaker:** Michael Hardy, VP Alliances & OEM, Quantum Corp
> — **Key Takeaway:** Buying rank: 1. Loaded TCO vs Tape/HDD, 2. Ingestion Write Speed, 3. Read Speed, 4. Time to first byte (acceptable in minutes).
> — **Source File:** `GLG_Interview_Michael_Hardy_Quantum_2026_07_17.pdf` (2026-07-26)

> **Quote #3:** “A tape cartridge, you can get 18 terabytes of tape for 100 bucks. Actually for 90 bucks... The problem with that is if you don't include the tape library—if you include the tape library, now you're up to about $500 per cartridge. It's 5x just to put it in a tape library. The cost of tape drives have gone up close to 75% now for enterprise tape drives... Cost of a library, it's $400 a slot roughly.”
> 
> — **Speaker:** Michael Hardy, VP Alliances & OEM, Quantum Corp
> — **Key Takeaway:** Raw tape media ($5/TB) balloons 5x to ~$25-$30/TB loaded TCO when robot library slots ($400/slot) and drives are included.
> — **Source File:** `GLG_Interview_Michael_Hardy_Quantum_2026_07_17.pdf` (2026-07-26)

> **Quote #4:** “Number one factor is definitely the cost. Per gigabyte how many cents I'm paying... and storage capacity density, those are the top number one factor... The second factor is the operational cost [power & idle sleep power]... The number three factor is operational useful life—are they going to have useful life which can go beyond five years or seven years?”
> 
> — **Speaker:** Dinesh Kumar, Former Procurement & Supply Chain Lead, Meta & AWS
> — **Key Takeaway:** Procurement priority rank: #1. Cost/GB & Form-factor Density (128TB-560TB+), #2. Power Consumption (idle power), #3. Useful Lifespan (10+ yrs).
> — **Source File:** `GLG_Interview_Dinesh_Kumar_Meta_AWS_2026_07_21.pdf` (2026-07-26)

> **Quote #5:** “The TCO for a hard drive includes the cost of the hard drive itself, which could be talked about in terms of gigabyte, like we are talking about $0.03-0.04 per gigabyte... The major value that HDD provide in terms of keeping their TCO competitive is because the per gigabyte cost of the hard drive are significantly lower compared to SSDs or memory.”
> 
> — **Speaker:** Dinesh Kumar, Former Procurement & Supply Chain Lead, Meta & AWS
> — **Key Takeaway:** Raw HDD cost benchmark sits at $0.03-$0.04/GB ($30-$40/TB), setting the hurdle raw cost for new cold storage media.
> — **Source File:** `GLG_Interview_Dinesh_Kumar_Meta_AWS_2026_07_21.pdf` (2026-07-26)


## 📌 5. Adoption & Commercial Strategy
*POC requirements, testing timelines, cloud decision-making, and deployment logistics*

> **Quote #1:** “Before placing any production petabytes on a non-standard physical medium, we need a 6-month hardware reliability POC in our own rack with standard S3-compatible API wrappers.”
> 
> — **Speaker:** Chief Technology Officer, Media Archive Group
> — **Key Takeaway:** S3-compatible API interface is non-negotiable for low-risk POCs.
> — **Source File:** `media_broadcaster_poc.txt` (2026-07-24)

> **Quote #2:** “If a new medium offered similar performance to HDD at half the cost, it could capture up to half of the HDD market. For tape, if the new medium offered a time to first byte of 1-10 seconds and similar TCO, it could capture 100% of the hyperscale market, which is expected to be 80% of the tape market in three years.”
> 
> — **Speaker:** Michael Hardy, VP Alliances & OEM, Quantum Corp
> — **Key Takeaway:** Market opportunity: 50% capture of HDD market at half cost; 100% capture of Hyperscale tape if latency drops to 1-10 seconds at equal TCO.
> — **Source File:** `GLG_Interview_Michael_Hardy_Quantum_2026_07_17.pdf` (2026-07-26)

> **Quote #3:** “Tape is environmentally sensitive. You have to keep the humidity in a certain range or tape gets wider. And when tape gets wider, you have to adjust the head inside the tape drive to make sure you're still able to track the data... If you have too dry of a situation when you've got magnetic media flying over a piece of metal and if there's no humidity in the air, things start sparking.”
> 
> — **Speaker:** Michael Hardy, VP Alliances & OEM, Quantum Corp
> — **Key Takeaway:** Narrow operating humidity window required for physical tape media; solid-state/glass mediums bypass strict atmospheric HVAC controls.
> — **Source File:** `GLG_Interview_Michael_Hardy_Quantum_2026_07_17.pdf` (2026-07-26)

> **Quote #4:** “If we are evaluating a new technology from a hard drive vendor... first show high level design spec & Delta list... vendor builds physical sample (4-8 weeks)... Meta engineering performance validation & extreme corner case testing (8-12 weeks)... deploy limited pilot of 200 to 500 units in operating data center (up to 12 weeks)... ALCT testing... mass production order of 100,000 units/quarter.”
> 
> — **Speaker:** Dinesh Kumar, Former Procurement & Supply Chain Lead, Meta & AWS
> — **Key Takeaway:** 4-5 month evaluation timeline from spec review to 200-500 unit pilot before 100,000 unit/quarter mass production order.
> — **Source File:** `GLG_Interview_Dinesh_Kumar_Meta_AWS_2026_07_21.pdf` (2026-07-26)

> **Quote #5:** “Whenever a hard drive vendor is trying to introduce a significant technological step function, there are always plans wherein Meta team will be visiting the OEMs factory to understand their processes... raw material, tooling, metal parts, compliance related to EHS and ESG compliance... then Accelerated Life Cycle Testing (ALCT).”
> 
> — **Speaker:** Dinesh Kumar, Former Procurement & Supply Chain Lead, Meta & AWS
> — **Key Takeaway:** Mandatory OEM factory visits for ESG/lead-free raw material compliance + Accelerated Life Cycle Testing (ALCT) prior to purchase order.
> — **Source File:** `GLG_Interview_Dinesh_Kumar_Meta_AWS_2026_07_21.pdf` (2026-07-26)
