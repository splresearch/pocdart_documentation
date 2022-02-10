# Scrum Rules and Policies:

Scrum is a highly collaborative framework for developing, delivering, and sustaining products, usually segmented into two-week cycles.

If you have questions about what a term may mean, please refer to the [Glossary](#glossary).

## Table of Contents:

- [Scrum Rules and Policies:](#scrum-rules-and-policies)
  - [Table of Contents:](#table-of-contents)
  - [Goals:](#goals)
- [Two-week Sprint Cycle:](#two-week-sprint-cycle)
  - [Meeting Types:](#meeting-types)
    - [Daily Sprint Huddle:](#daily-sprint-huddle)
    - [Data Engineer Workshop:](#data-engineer-workshop)
    - [Post-mortem:](#post-mortem)
    - [Discovery Block:](#discovery-block)
    - [Sprint Retrospective:](#sprint-retrospective)
    - [Sprint Planning:](#sprint-planning)
  - [Trello Cards:](#trello-cards)
- [Glossary](#glossary)

## Goals:

- Decrease Distractions
- Control Work-in-Progress
- Promote Teamwork
- Improve Efficiency and Throughput
- Decrease Bottlenecks

# Two-week Sprint Cycle:

|| Monday | Tuesday | Wednesday | Thursday | Friday
|---|---|---|---|---|---|
| Week 1 | Data Engineer Workshop, Huddle, Post-mortem, Discovery Block | Sprint Retrospective, Sprint Planning | Huddle | Huddle | Huddle, Discovery Block |
| Week 2 | Data Engineer Workshop, Huddle, Discovery Block | Huddle | Huddle | Huddle | Huddle, Discovery Block |

## Meeting Types:

As seen in above table, there are various types of meetings in every Sprint:

### Daily Sprint Huddle:

This is one of the backbones of the Scrum process. Standing up is recommended for this process but not obligated in remote-work settings.

These meetings begin with discussing any open tickets in the `dmar-support` channel, exceptional errors in the `dart_error_reports` channel, and anything else outstanding in Slack that the rest of the team should be made aware of.

The next portion is checking the status of the Sprint board. Each card that is not in either the "To-Do", "Done", or "Monitoring" columns are gone over by their respective Owners. Each Owner or major contributor will give the status of said card. If required, there can be follow-up meetings about certain cards should they demand enough attention from those involved.

### Data Engineer Workshop:

This is a meeting between all of the Data Engineers, ranging about an hour before a Huddle.

In this meeting, the general conversation pertains around discussing what work is left on the Sprint board, who can help with completing the unfinished cards, how those cards can be accomplished, and general statuses of the Data Engineers.

### Post-mortem:

This is usually done in conjunction with a Huddle.

In this section, unplanned work cards are reexplained and a group discussion begins with how to answer the two following questions:

1. How can the cause for this unplanned work be prevented in future?
2. What monitoring can be setup to detect this issue as fast as possible?

Once both are answered for all completed Post-mortem cards, the cards are either retired for the Sprint or put into "Monitoring".

### Discovery Block:

This occurs after some Huddles.

During this time, one should meet and discuss with other team members about any cards in the "DISCOVERY" Board.

The purpose of the block is to do research or complete any other prerequisite for a particular card(s) so that they may be put into the "READY FOR SPRINT" column.

### Sprint Retrospective:

This occurs on the same day as Sprint Planning.

This portion of the meeting usually includes the presentation of completed cards by either Owners or major contributors of a card and the counting of Story Points.

There are also discussions of what went well during the Sprint, what parts could be improved upon, and other retrospective bits of information

Following a Sprint Retrospective, there is a break before moving on to the Sprint Planning phase of the meeting.

### Sprint Planning:

This always occurs after a Sprint Retrospective.

This portion of the meeting includes the allocating of total Story Points for next Sprint and transferring over of priority cards respective to their Owners.

This is also where team members will alert other team members of any expected PTO that will be taken during planned Sprint.

## Trello Cards:

Trello is used to visualize and help facilitate our workflow through the use of its "cards".

Before releasing any cards, each one must fulfill each of the following requirements:

1. There must some Owner assigned to the card.
2. There must some Description of the problem or desired result from the card.
3. To-do lists, contained tasks with appropriately assigned people.
4. Range of dates for when the card could be placed into the Sprint board.
5. Definition of Done.
6. Number of Story Points needed to complete the Definition of Done.

# Glossary

Sprint
: Sprint

Owner
: Owner
