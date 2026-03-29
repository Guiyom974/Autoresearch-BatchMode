
### Query: mathematical models for constructing characteristic functions in cooperative games with superadditivity and monotonicity constraints
## Mathematical Models for Constructing Characteristic Functions in Cooperative Games with Superadditivity and Monotonicity Constraints

In cooperative game theory, the characteristic function is a fundamental concept that assigns a value to each possible coalition of players, representing the payoff that coalition can guarantee for itself. Constructing these functions often involves adhering to certain constraints, such as superadditivity and monotonicity, which reflect the nature of cooperation and potential gains.

Here's a summary of mathematical models and concepts related to constructing characteristic functions with these constraints:

*   **Definition of a Characteristic Function Game:** A cooperative game is formally defined by a pair $(N, v)$, where $N$ is the set of players and $v$ is the characteristic function. This function, $v: 2^N \rightarrow \mathbb{R}$, maps every subset of players (a coalition) to a real-valued payoff [[1]](https://kam.mff.cuni.cz/~cerny/data/CG/CG7-generalised-models_handout.pdf)[[2]](https://www.cs.cmu.edu/afs/cs/academic/class/15859-s05/www/ferguson/coal.pdf). The value $v(S)$ represents what coalition $S$ can achieve on its own [[3]](https://fiveable.me/game-theory-economic-behavior/unit-9/cooperative-games-characteristic-functions/study-guide/RTHtWJ5IIuQVUfjj). It is conventionally assumed that $v(\emptyset) = 0$ [[2]](https://www.cs.cmu.edu/afs/cs/academic/class/15859-s05/www/ferguson/coal.pdf)[[4]](https://www.lamsade.dauphine.fr/~airiau/Teaching/CoopGames/2012/lecture1.pdf).

*   **Superadditivity:** A game is superadditive if the value of the union of two disjoint coalitions is greater than or equal to the sum of their individual values. Mathematically, for any disjoint coalitions $S$ and $T$, $v(S \cup T) \geq v(S) + v(T)$ [[3]](https://fiveable.me/game-theory-economic-behavior/unit-9/cooperative-games-characteristic-functions/study-guide/RTHtWJ5IIuQVUfjj)[[5]](https://vknight.org/Year_3_game_theory_course/Content/Chapter_16_Cooperative_games/). This property implies that players have an incentive to form larger coalitions, as cooperation is at least as beneficial as acting separately [[3]](https://fiveable.me/game-theory-economic-behavior/unit-9/cooperative-games-characteristic-functions/study-guide/RTHtWJ5IIuQVUfjj)[[6]](https://ccc.cs.uni-duesseldorf.de/~rothe/SPIELTHEORIE/folien-6-cooperative-games-foundations.pdf). If the characteristic function is non-negative, superadditivity implies monotonicity [[4]](https://www.lamsade.dauphine.fr/~airiau/Teaching/CoopGames/2012/lecture1.pdf)[[7]](https://www.utdallas.edu/~chandra/documents/6311/coopgames.pdf).

*   **Monotonicity:** A game is monotonic if for any two coalitions $S$ and $T$, where $S$ is a subset of $T$, the value of $S$ is less than or equal to the value of $T$ ($v(S) \leq v(T)$ for $S \subseteq T$) [[5]](https://vknight.org/Year_3_game_theory_course/Content/Chapter_16_Cooperative_games/)[[8]](https://en.wikipedia.org/wiki/Cooperative_game_theory). This means that a larger coalition is always at least as valuable as a smaller one [[9]](https://www.researchgate.net/publication/254418014_A_note_on_the_monotonicity_and_superadditivity_of_TU_cooperative_games). While superadditivity implies monotonicity (given non-negative values), the converse is not always true; there exist monotonic games that are not superadditive [[6]](https://ccc.cs.uni-duesseldorf.de/~rothe/SPIELTHEORIE/folien-6-cooperative-games-foundations.pdf)[[9]](https://www.researchgate.net/publication/254418014_A_note_on_the_monotonicity_and_superadditivity_of_TU_cooperative_games). Non-monotonicity can arise from factors like players disliking each other or increasing communication overheads with coalition size [[4]](https://www.lamsade.dauphine.fr/~airiau/Teaching/CoopGames/2012/lecture1.pdf)[[7]](https://www.utdallas.edu/~chandra/documents/6311/coopgames.pdf).

*   **Construction Approaches:**
    *   **Direct Definition:** The characteristic function can be directly defined for all possible coalitions. This is feasible for a small number of players but becomes computationally expensive as the number of coalitions grows exponentially ($2^n$ for $n$ players) [[1]](https://kam.mff.cuni.cz/~cerny/data/CG/CG7-generalised-models_handout.pdf)[[2]](https://www.cs.cmu.edu/afs/cs/academic/class/15859-s05/www/ferguson/coal.pdf).
    *   **Superadditive Cover:** For a given game $G$, its superadditive cover $G^*$ is constructed such that $v^*(T)$ is the maximum value players in set $T$ can achieve by forming their own coalition structure [[7]](https://www.utdallas.edu/~chandra/documents/6311/coopgames.pdf).
    *   **Differential Games:** In cooperative differential games, characteristic functions can be constructed by first finding optimal control strategies that maximize total payoff for a coalition, and then having non-coalition members use strategies that minimize the coalition's payoff. This method often results in superadditive characteristic functions [[10]](https://www.researchgate.net/publication/319674815_On_an_approach_to_constructing_a_characteristic_function_in_cooperative_differential_games)[[11]](https://discovery.researcher.life/article/on-the-superadditivity-of-a-characteristic-function-in-cooperative-differential-games-with-negative-externalities/10b56ae68538394a84bbcb7f76ee5db9).
    *   **Interval Games:** For games with uncertainty, interval characteristic functions are used, where the value of a coalition is an interval rather than a scalar. Algorithms exist to define these interval values, often based on solving zero-sum interval games [[12]](https://www.gerad.ca/fr/papers/G-2024-14.pdf)[[13]](https://www.aimsciences.org/data/article/export-pdf?doi=10.3934/jdg.2024019).

*   **Properties and Implications:**
    *   Superadditivity suggests that the grand coalition (all players together) will likely form, as there's always a benefit to merging [[6]](https://ccc.cs.uni-duesseldorf.de/~rothe/SPIELTHEORIE/folien-6-cooperative-games-foundations.pdf)[[14]](https://cw.fel.cvut.cz/old/_media/courses/ae4m36mas/mas2013-l08-cooperative_games.pdf).
    *   Monotonicity ensures that adding more players to a coalition does not decrease its potential payoff [[5]](https://vknight.org/Year_3_game_theory_course/Content/Chapter_16_Cooperative_games/)[[9]](https://www.researchgate.net/publication/254418014_A_note_on_the_monotonicity_and_superadditivity_of_TU_cooperative_games).
    *   Convex games, which are a subset of superadditive games, have the property that the marginal contribution of a player increases with the size of the coalition they join [[3]](https://fiveable.me/game-theory-economic-behavior/unit-9/cooperative-games-characteristic-functions/study-guide/RTHtWJ5IIuQVUfjj)[[4]](https://www.lamsade.dauphine.fr/~airiau/Teaching/CoopGames/2012/lecture1.pdf).

In practice, the choice of model and the method for constructing the characteristic function depend on the specific problem and the assumptions about player behavior and the nature of cooperation.

---
Learn more:
1. [Cooperative game theory](https://kam.mff.cuni.cz/~cerny/data/CG/CG7-generalised-models_handout.pdf)
2. [GAME THEORY](https://www.cs.cmu.edu/afs/cs/academic/class/15859-s05/www/ferguson/coal.pdf)
3. [Cooperative games and characteristic functions - Fiveable](https://fiveable.me/game-theory-economic-behavior/unit-9/cooperative-games-characteristic-functions/study-guide/RTHtWJ5IIuQVUfjj)
4. [Lecture 1 - Introduction and Definition of TU games - Lamsade](https://www.lamsade.dauphine.fr/~airiau/Teaching/CoopGames/2012/lecture1.pdf)
5. [Chapter 16 - Cooperative games - Vincent Knight](https://vknight.org/Year_3_game_theory_course/Content/Chapter_16_Cooperative_games/)
6. [Algorithmische Spieltheorie Foundations of Cooperative Game Theory Wintersemester 2022/2023 - HHU](https://ccc.cs.uni-duesseldorf.de/~rothe/SPIELTHEORIE/folien-6-cooperative-games-foundations.pdf)
7. [Cooperative Game Theory](https://www.utdallas.edu/~chandra/documents/6311/coopgames.pdf)
8. [Cooperative game theory - Wikipedia](https://en.wikipedia.org/wiki/Cooperative_game_theory)
9. [A note on the monotonicity and superadditivity of TU cooperative games - ResearchGate](https://www.researchgate.net/publication/254418014_A_note_on_the_monotonicity_and_superadditivity_of_TU_cooperative_games)
10. [On an approach to constructing a characteristic function in cooperative differential games | Request PDF - ResearchGate](https://www.researchgate.net/publication/319674815_On_an_approach_to_constructing_a_characteristic_function_in_cooperative_differential_games)
11. [On the superadditivity of a characteristic function in cooperative differential games with negative externalities - R Discovery](https://discovery.researcher.life/article/on-the-superadditivity-of-a-characteristic-function-in-cooperative-differential-games-with-negative-externalities/10b56ae68538394a84bbcb7f76ee5db9)
12. [Characteristic functions for cooperative interval games - GERAD](https://www.gerad.ca/fr/papers/G-2024-14.pdf)
13. [CHARACTERISTIC FUNCTIONS FOR COOPERATIVE INTERVAL GAMES Elena M. Parilina - American Institute of Mathematical Sciences](https://www.aimsciences.org/data/article/export-pdf?doi=10.3934/jdg.2024019)
14. [Cooperative Game Theory](https://cw.fel.cvut.cz/old/_media/courses/ae4m36mas/mas2013-l08-cooperative_games.pdf)



### Query: deterministic algorithms for generating $2^N-1$ coalition values in minimal N-player cooperative games
The concept of generating $2^N-1$ coalition values in N-player cooperative games is fundamental to cooperative game theory. These values represent the worth or utility that each possible coalition of players can achieve [[1]](https://yung-web.github.io/home/courses/game_files/13.SV-4.pdf)[[2]](https://yung-web.github.io/home/courses/game_files/13.SV.pdf). While the problem of defining and calculating these values is well-established, the focus of research often lies in specific solution concepts or algorithms for determining outcomes, such as the Shapley value [[1]](https://yung-web.github.io/home/courses/game_files/13.SV-4.pdf)[[3]](https://pureadmin.qub.ac.uk/ws/portalfiles/portal/476504515/A_new_value.pdf), or analyzing properties like the core [[2]](https://yung-web.github.io/home/courses/game_files/13.SV.pdf)[[4]](https://en.wikipedia.org/wiki/Cooperative_game_theory).

Deterministic algorithms for generating all possible coalition values in minimal N-player cooperative games are not explicitly detailed as a distinct algorithmic category in the provided search results. However, the underlying principles and methods for defining and working with these games provide a framework from which such algorithms could be derived.

Key aspects relevant to generating coalition values include:

*   **Characteristic Function:** The core of a cooperative game is the characteristic function, denoted as $v(S)$, which assigns a real-valued payoff to every possible coalition $S$ of players [[1]](https://yung-web.github.io/home/courses/game_files/13.SV-4.pdf)[[5]](https://cw.fel.cvut.cz/old/_media/courses/ae4m36mas/mas2013-l08-cooperative_games.pdf). The generation of $2^N-1$ coalition values essentially means defining or computing the value for every non-empty subset of players.
*   **Transferable Utility (TU) Games:** In TU games, the worth of a coalition can be freely redistributed among its members [[1]](https://yung-web.github.io/home/courses/game_files/13.SV-4.pdf)[[3]](https://pureadmin.qub.ac.uk/ws/portalfiles/portal/476504515/A_new_value.pdf). This assumption simplifies the calculation and analysis of coalition values.
*   **Superadditivity and Convexity:** Properties like superadditivity (where the value of the union of disjoint coalitions is at least the sum of their individual values) and convexity (a stronger condition) are often assumed or analyzed in cooperative games, influencing how coalition values might be structured or generated [[1]](https://yung-web.github.io/home/courses/game_files/13.SV-4.pdf)[[2]](https://yung-web.github.io/home/courses/game_files/13.SV.pdf).

While specific deterministic algorithms for exhaustively generating all $2^N-1$ values for minimal N-player games are not directly presented, the process of defining a cooperative game inherently involves specifying these values. For instance, in a weighted voting game, the value of a coalition is determined by the sum of votes it possesses, and a threshold for winning [[6]](https://ics-websites.science.uu.nl/docs/vakken/mas/slides/cooperativegame.pdf)[[7]](https://comsoc-community.org/archive/estoril-2010/slides/Aziz.pdf). In graph games, coalition values are derived from the structure and weights of edges within the induced subgraph of the coalition [[8]](https://cdn.aaai.org/ojs/8653/8653-13-12181-1-2-20201228.pdf).

Research in this area often focuses on more complex problems like coalition structure generation [[8]](https://cdn.aaai.org/ojs/8653/8653-13-12181-1-2-20201228.pdf)[[9]](https://www.cs.cmu.edu/~conitzer/coalitionJAAMAS18.pdf) or analyzing the properties of specific solution concepts rather than the brute-force generation of all coalition values, which can be computationally intensive for larger N. The term "minimal N-player cooperative games" might imply a focus on games with a limited number of players or specific structural properties, but the search results do not provide specialized algorithms for this exact scenario.

---
Learn more:
1. [Lecture 13: Cooperative Game Theory Coalition Game - GitHub Pages](https://yung-web.github.io/home/courses/game_files/13.SV-4.pdf)
2. [Lecture 13: Cooperative Game Theory Coalition Game - GitHub Pages](https://yung-web.github.io/home/courses/game_files/13.SV.pdf)
3. [A new value for cooperative games based on coalition size - Queen's University Belfast](https://pureadmin.qub.ac.uk/ws/portalfiles/portal/476504515/A_new_value.pdf)
4. [Cooperative game theory - Wikipedia](https://en.wikipedia.org/wiki/Cooperative_game_theory)
5. [Cooperative Game Theory](https://cw.fel.cvut.cz/old/_media/courses/ae4m36mas/mas2013-l08-cooperative_games.pdf)
6. [Introduction to Coalitional Game Theory](https://ics-websites.science.uu.nl/docs/vakken/mas/slides/cooperativegame.pdf)
7. [Monotone cooperative games and their threshold versions](https://comsoc-community.org/archive/estoril-2010/slides/Aziz.pdf)
8. [Optimal Coalition Structure Generation in Cooperative Graph Games - Association for the Advancement of Artificial Intelligence (AAAI)](https://cdn.aaai.org/ojs/8653/8653-13-12181-1-2-20201228.pdf)
9. [Coalition structure generation in cooperative games with compact representations - CMU School of Computer Science](https://www.cs.cmu.edu/~conitzer/coalitionJAAMAS18.pdf)



### Query: query three here
In database management, "querying" refers to the process of retrieving information from a database. This can involve simple requests for specific data or complex operations that combine data from multiple tables.

Here's a summary of how to approach queries, particularly when dealing with multiple tables or complex requirements:

### Types of Queries and Their Applications

*   **Action Queries:** These queries perform an action on the data, such as inserting, updating, or deleting records. For example, you might use a delete query to remove a specific row from a table based on a unique identifier. [[1]](https://www.youtube.com/watch?v=LYy2kkBDOdw)
*   **Cross-Tab Queries:** These queries reorganize and summarize data, presenting it in a grid format with rows and columns. They are useful for analyzing data by categories, such as counting occurrences within specific intersections of data. [[1]](https://www.youtube.com/watch?v=LYy2kkBDOdw)
*   **Multi-Criterion Queries:** These queries allow you to retrieve data based on multiple conditions. For instance, you could find all doctors whose last name is "Miller" and whose specialty is "Pediatrics." [[1]](https://www.youtube.com/watch?v=LYy2kkBDOdw)

### Querying Across Multiple Tables

When dealing with data spread across several tables, SQL (Structured Query Language) provides methods to join them and retrieve comprehensive results.

*   **JOIN Clauses:** SQL's `JOIN` clauses are fundamental for combining rows from two or more tables based on a related column between them. Different types of joins (e.g., `INNER JOIN`, `LEFT JOIN`) determine which rows are included in the result set based on whether matches are found in all tables. [[2]](https://stackoverflow.com/questions/41395968/how-to-find-all-details-from-three-different-tables-in-sql)[[3]](https://www.youtube.com/watch?v=9mw1aNk1gfk)
*   **Combining Detail Tables:** In scenarios with a "header" table and multiple "detail" tables, you can use techniques like `UNION` to consolidate data from the detail tables before joining it with the header. This ensures that all relevant details are retrieved, even if some headers have no corresponding entries in certain detail tables. [[4]](https://www.youtube.com/watch?v=sNeMSh2Ngz0)
*   **Step-by-Step Approach:** A recommended method for joining multiple tables is to start with two tables, verify the results, and then incrementally add more tables. This approach helps in managing complexity and identifying issues early on. [[3]](https://www.youtube.com/watch?v=9mw1aNk1gfk)

### Querying in Specific Contexts

*   **Writing Query Letters:** In the context of writing, a "query letter" is a document sent to literary agents or editors to pitch a manuscript. A strong query letter typically includes a concise summary of the book, key plot points, and a brief author bio, designed to pique interest without revealing the entire story. [[5]](https://www.writersdigest.com/improve-my-writing/basics-of-a-solid-3-paragraph-query)[[6]](https://www.query101.blog/blog/the-query-letter-summary)
*   **Mobile Carrier Services:** For some mobile carriers, like "Three," a feature called "Your Queries" might exist to track customer inquiries or complaints. However, this feature may be an older one and could have been removed or relocated within their service platforms. [[7]](https://community.three.co.uk/t5/Account-and-services/How-do-you-find-your-query-s-On-three/m-p/46744)[[8]](https://community.three.co.uk/t5/Account-and-services/Your-Queries-where-is-it/m-p/52436)

---
Learn more:
1. [Creating Three Queries - YouTube](https://www.youtube.com/watch?v=LYy2kkBDOdw)
2. [How to find all details from three different tables in SQL? - Stack Overflow](https://stackoverflow.com/questions/41395968/how-to-find-all-details-from-three-different-tables-in-sql)
3. [SQL Joins: 3+ Tables Made Simple - YouTube](https://www.youtube.com/watch?v=9mw1aNk1gfk)
4. [How to Query Header and Multiple Detail Tables in SQL Server Efficiently - YouTube](https://www.youtube.com/watch?v=sNeMSh2Ngz0)
5. [Basics of a Solid 3-Paragraph Query - Writer's Digest](https://www.writersdigest.com/improve-my-writing/basics-of-a-solid-3-paragraph-query)
6. [The Query Letter Summary](https://www.query101.blog/blog/the-query-letter-summary)
7. [Solved: Re: How do you find your query's. On three](https://community.three.co.uk/t5/Account-and-services/How-do-you-find-your-query-s-On-three/m-p/46744)
8. ['Your Queries' - where is it? - Three Community - 52436](https://community.three.co.uk/t5/Account-and-services/Your-Queries-where-is-it/m-p/52436)


