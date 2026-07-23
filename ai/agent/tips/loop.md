## Context engineering so far

- agent memory
  - CLAUDE.md
  - memory tool
    - memory_read()
    - memory_write()
    - memory_edit()
  - skills
  - memory/
    - notes/
    - deploy.md
    - team-rules.md
    - Files read and writen by agents
- skills
  - progress disclosure
- memory/ systems
  - using file systems
- lessons so far
  - format
    - CLAUDE.md, skills, memory/*.md
  - reading
    - frontmatter + grep
  - writing
    - autonomy wins
      - agents do best when free to record what they deem relevant, how they see fit.
    - continuous learning

## The state of the art in memory today

- scaling memory
  - concurrent writes
  - lost attribution
  - stale & mixed scopes
- versioning & concurrency
  - precondition hash
- portability
- In-band memory reaches its limits
  - memories go stale

## Dreaming up the path to continual learning

- Dream up
  - （突飛なアイデアや計画などを）思いつく」「考え出す」「ひらめく」
- **Introducing Dreaming**
  - A batch process that runs out of band
    - - with a single objective os curating memory.

