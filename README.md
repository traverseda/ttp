# Time Tracker Plus

`ttp`, a time tracker inspired by `utt`.

Frankly it's also a good resume piece, as it's small enough to read easily,
small enough that it didn't take too much time to complete to a "proffesional"
standard (documentation pending), and complicated enough that it demonstrates a
general understanding of complicated issues like time zones, templating, etc. A
lot better then most of what I have on github, which tend towards incomplete
experements.

It's not complicated, but it is more readable than the average data-science
pipeline, and more of a complete product than most of what I get called on to
make proffesionally.

---

ttp is a python time tracker where you tell the time
tracker what you've done *after* you've already done it. Like writing a git
commit message.

start tracking time with `ttp start`, then when you've finished a task add it
with `ttp add updated my resume`. You can edit your log with `ttp edit`.

`ttp project someproject` changes what project you're logging to.

`ttp report` shows a report of your current tasks. Help is wanted for this, as
we need more template options. Uses jinja2 for templating.

## Instalation

```
pip install pipx --user
pipx install time-tracker-plus
```

Optionally enable bash's tab-completion by adding this to your `~/.bashrc` file.

`eval "$(_TTP_COMPLETE=source ttp)"`

## Example report

You can write new reports using jinja2. Personally I use this to generate
invoices for clients, directly from my hours.

This is with the `default.md` template.

```markdown
# default
## Monday, January 20th, 2020 to Sunday, January 26th, 2020

 *  1.00h worked on time tracker
 *  4.00h worked on time tracker2
 * 22.00h worked on time tracker3
 *  1.88h worked on time tracker overnight

28.88 hours worked total
```
