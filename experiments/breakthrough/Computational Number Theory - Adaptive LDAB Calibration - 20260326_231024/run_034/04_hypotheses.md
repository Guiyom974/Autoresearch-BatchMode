**Hypothesis 1 – Pre‑request overflow detection cuts timeout rates for large‑k primorial gap calculations**  
*Statement*: Adding a dedicated overflow‑check step before an API request is issued will dramatically reduce the number of time‑outs that occur when the computation is extended beyond the already‑robust region (k ≤ 8).  

*Why it’s testable*: Overflow detection can be turned on/off in the client pipeline, and the outcome (timeout vs. success) is directly observable for each request.  

*Experiment*:  
1. **Baseline** – Run the existing “no‑overflow‑check” pipeline for a set of k values that are known to cause time‑outs (e.g., k = 9, 10, 12, 15). Record the number of time‑outs per k.  
2. **Enhanced** – Insert an overflow‑pre‑check (e.g., test whether any intermediate product would exceed the current numeric‐type limit) immediately before the same API call. Repeat the same k‑set.  
3. **Comparison** – Compute the timeout‑rate reduction (timeouts / total requests) for each k and test for a statistically significant drop (McNemar’s test).  

*Rationale*: Prior work showed that the pipeline works reliably up to k = 8, but overflow artefacts appear at k ≥ 9. Detecting and preventing overflow before the request should avoid the retries that generate time‑outs.

---

**Hypothesis 2 – A sigmoid relationship exists between primorial index k and the probability of a request time‑out**  
*Statement*: The likelihood that a fixed‑timeout API request will time out rises sharply after a characteristic k (the “critical k”), following a logistic (sigmoid) curve rather than a simple linear increase.  

*Why it’s testable*: By running many repeated trials at each k we can estimate the timeout probability P(timeout|k) and fit a logistic model to the data.  

*Experiment*:  
1. Issue 100 independent API calls for VMR(k) at k = 2, 3, …, 20, using the same server‑side timeout (e.g., 30 s).  
2. Record the number of successes vs. time‑outs for each k.  
3. Fit a logistic regression:  P(timeout) = 1 / (1 + exp[‑(α + β · k)]) + error, and test whether β > 0 (significant increase) and locate the inflection point (critical k).  

*Link to prior findings*: The observed “sharp VMR drop” at k = 8 may correspond to the point where the timeout probability begins to rise steeply; this hypothesis formalises that observation.

---

**Hypothesis 3 – Chunked (checkpointed) computation lowers per‑request load and reduces time‑outs**  
*Statement*: Splitting a high‑k primorial‑gap VMR calculation into several smaller sub‑requests (e.g., compute the product of the first half of the primorial, checkpoint the result, then compute the second half) will reduce the computational load of each individual request, thereby decreasing the chance of a time‑out while preserving the final result.  

*Why it’s testable*: The chunk size can be varied systematically, and timeout occurrence can be measured for each chunk configuration.  

*Experiment*:  
1. Identify a k that consistently times out when issued as a single request (e.g., k = 12).  
2. Issue the same computation in three modes:  
   - **Monolithic** – one request for the full k = 12 VMR.  
   - **Two‑chunk** – split at the midpoint (k = 6 + 6).  
   - **Four‑chunk** – split at k = 3 + 3 + 3 + 3.  
3. For each mode run 30 trials, record the per‑request timeout rate and the overall success rate.  
4. Use a χ² test to determine whether chunking significantly reduces time‑outs.  

*Prior context*: Prior work noted that overflow/truncation artefacts at k ≥ 9 force retries; breaking the work into smaller pieces avoids triggering the server’s time‑limit threshold.

---

**Hypothesis 4 – A runtime‑prediction model enables dynamic timeout windows that lower overall timeout rates**  
*Statement*: By training a simple regression model on observed execution times for small k (e.g., k ≤ 8) we can predict the expected runtime for larger k and automatically set a per‑request timeout that is just long enough (plus a safety margin). This adaptive policy will yield fewer time‑outs than a static, conservative timeout.  

*Why it’s testable*: The prediction algorithm and the adaptive timeout can be implemented in the client, and the resulting timeout frequency is directly measurable.  

*Experiment*:  
1. **Training set** – For k = 2,…,8, record the actual server‑side elapsed time for successful VMR computations (e.g., from server‑returned metadata).  
2. **Model** – Fit a linear (or power‑law) regression:  time ≈ a·kᵇ + c.  
3. **Deployment** – For each request with k > 8, set the client‑side timeout to  predicted_time × 1.2 (20 % margin).  
4. **Control** – Run the same k‑set with a fixed conservative timeout (e.g., 60 s).  
5. **Comparison** – Record timeout rates and total wall‑clock time for both strategies; test for a lower timeout rate with the adaptive method (paired‑t test on the difference).  

*Rationale*: Prior analyses showed that the scaling exponent of VMR (≈ 0.80) is lower than earlier guesses, implying that runtime growth is sub‑exponential; a data‑driven timeout can capture this more accurately than a one‑size‑fits‑all limit.

---

**Hypothesis 5 – Switching to arbitrary‑precision arithmetic eliminates overflow‑induced VMR artefacts and therefore reduces retry‑driven time‑outs**  
*Statement*: Using a true arbitrary‑precision integer library (e.g., GMP, Python’s `int`, or `decimal`) instead of floating‑point or fixed‑width integers will prevent the overflow/truncation that produces the spurious VMR dip at k = 8, eliminating the need for client‑side retries that often cause time‑outs.  

*Why it’s testable*: The numeric representation can be toggled in the code, and both the VMR values and the number of retries/time‑outs can be recorded.  

*Experiment*:  
1. **Baseline** – Compute VMR(k) for k = 9,…,15 using the current floating‑point implementation (which overflows). Monitor the retry count and timeout events.  
2. **Precision‑enhanced** – Re‑implement the same algorithm with GMP (or Python’s unlimited‑size integers) and repeat the same k‑set.  
3. **Metrics** – Compare:  
   - Mean VMR (to confirm the dip disappears).  
   - Number of retries per request.  
   - Overall timeout rate.  
4. **Statistical test** – Use a two‑sample proportion test to see whether the precision switch yields a significantly lower timeout proportion.  

*Connection to prior work*: The “sharp VMR drop at k = 8” was attributed to overflow/truncation; removing the root cause should flatten the VMR curve and prevent the retry loops that generate API time‑outs.  

---

### How these hypotheses together address the **“API error: Request timed out.”** problem  

| Hypothesis | Primary mitigation strategy | Expected impact on timeout rate |
|------------|-----------------------------|---------------------------------|
| 1 – Overflow detection | Prevent overflow before it reaches the server | **High** – eliminates a major source of retries |
| 2 – Sigmoid timeout model | Identify the critical k beyond which timeouts become likely | **Medium** – guides where to apply extra caution |
| 3 – Chunked computation | Reduce per‑request workload | **Medium‑High** – directly lowers load on each call |
| 4 – Dynamic timeout windows | Match timeout to actual runtime needs | **Medium** – reduces false‑negative timeouts |
| 5 – Arbitrary‑precision arithmetic | Remove numeric overflow artefacts | **High** – eliminates retries caused by VMR anomalies |

By testing these hypotheses we can pinpoint the dominant cause(s) of the time‑outs and implement a layered solution (pre‑check → adaptive sizing → dynamic timeout) that makes large‑k primorial‑gap computations reliable and scalable.