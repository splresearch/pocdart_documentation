# Scrum Rules and Policies

Scrum is a highly collaborative framework for developing, delivering, and sustaining products, usually segmented into two-week cycles.

If you have questions about what a term may mean, please refer to the [Glossary](#glossary).

## Table of Contents

- [Scrum Rules and Policies](#scrum-rules-and-policies)
  - [Table of Contents](#table-of-contents)
  - [Goals](#goals)
- [Two-week Sprint Cycle](#two-week-sprint-cycle)
  - [Meeting Types](#meeting-types)
    - [Daily Sprint Huddle](#daily-sprint-huddle)
    - [Data Engineer Workshop](#data-engineer-workshop)
    - [Post-mortem](#post-mortem)
    - [Discovery Block](#discovery-block)
    - [Sprint Retrospective](#sprint-retrospective)
      - [Sprint Celebration of Work](#sprint-celebration-of-work)
    - [Sprint Planning](#sprint-planning)
  - [Trello Cards](#trello-cards)
    - [Trello Cards Before Sprint](#trello-cards-before-sprint)
      - [Determinants for Work](#determinants-for-work)
      - [Card Templates](#card-templates)
      - [Card Labels](#card-labels)
      - [Assigning Story Points](#assigning-story-points)
      - [Finishing Creation of Card](#finishing-creation-of-card)
    - [Trello Cards After Sprint](#trello-cards-after-sprint)
      - [Card Story Points Adjustment Syntax](#card-story-points-adjustment-syntax)
      - [Card Story Points Counting](#card-story-points-counting)
- [Glossary](#glossary)

## Goals

- Decrease Distractions
- Control Work-in-Progress
- Promote Teamwork
- Improve Efficiency and Throughput
- Decrease Bottlenecks

# Two-week Sprint Cycle

|| Monday | Tuesday (Beginning of new Cycle) | Wednesday | Thursday | Friday
|---|---|---|---|---|---|
| Week 1 | Data Engineer Workshop, Huddle, Post-mortem, Discovery Block | Sprint Retrospective, Sprint Planning | Huddle | Huddle | Huddle, Discovery Block |
| Week 2 | Data Engineer Workshop, Huddle, Discovery Block | Huddle | Huddle | Huddle | Huddle, Discovery Block |

## Meeting Types

As seen in above table, there are various types of meetings in every Sprint.

The core meeting types include [Daily Sprint Huddle](#daily-sprint-huddle), [Post-mortem](#post-mortem), [Discovery Block](#discovery-block), [Sprint Retrospective](#sprint-retrospective), and [Sprint Planning](#sprint-planning).

### Daily Sprint Huddle

This is one of the backbones of the Scrum process. Standing up is recommended for this process but not obligated in remote-work settings.

These meetings begin with discussing any open tickets in the `dmar-support` channel, exceptional errors in the `dart_error_reports` channel, and anything else outstanding in Slack that the rest of the team should be made aware of.

The next portion is checking the status of the Sprint board. Each card that is not in either the "To-Do", "Done", or "Monitoring" columns are gone over by their respective Owners. Each Owner or major contributor will give the status of said card. If required, there can be follow-up meetings about certain cards should they demand enough attention from those involved.

### Data Engineer Workshop

This is a meeting between all of the Data Engineers, ranging about an hour before a Huddle.

In this meeting, the general conversation pertains around discussing what work is left on the Sprint board, who can help with completing the unfinished cards, how those cards can be accomplished, and general statuses of the Data Engineers.

### Post-mortem

This is usually done in conjunction with a Huddle.

In this section, unplanned work cards are reexplained and a group discussion begins with how to answer the two following questions:

1. How can the cause for this unplanned work be prevented in future?
2. What monitoring can be setup to detect this issue as fast as possible?

Once both are answered for all completed Post-mortem cards, the cards are either retired for the Sprint or put into "Monitoring".

### Discovery Block

This occurs after some Huddles.

During this time, one should meet and discuss with other team members about any cards in the "DISCOVERY" Board.

The purpose of the block is to do research or complete any other prerequisite for a particular card(s) so that they may be put into the "READY FOR SPRINT" column.

### Sprint Retrospective

This occurs on the same day as Sprint Planning.

There are also discussions of what went well during the Sprint, what parts could be improved upon, and other retrospective bits of information

Following a Sprint Retrospective, there is a break before moving on to the Sprint Planning phase of the meeting.

#### Sprint Celebration of Work

This is done during the Sprint Retrospective.

This portion of the meeting usually includes the presentation of completed cards by either Owners or major contributors of a card and the counting of Story Points.

### Sprint Planning

This always occurs after a Sprint Retrospective.

This portion of the meeting includes the allocating of total Story Points for next Sprint and transferring over of priority cards respective to their Owners.

This is also where team members will alert other team members of any expected PTO that will be taken during planned Sprint.

## Trello Cards

Trello is used to visualize and help facilitate our workflow through the use of its "cards".

### Trello Cards Before Sprint

Upon meeting all of the requirements for new work (listed below), a Trello Card can made on the "DISCOVERY" board.

#### Determinants for Work

The determinants for new work are as follows:

1. Identifiable and accessible business owner
2. Commitment from business owner
3. Strength of reqs on first contact / before the work is released
4. Value to department (political/infrastructure) vs. amount of development + maintenance + implementation work required

#### Card Templates

Trello cards must only be created from the following templates located on the left-most column "TEMPLATES":

- UNPLANNED work template
- User Story - New PoCDART project
- Change Requests
- Internal Work
- XSP New Measure or Alteration of Measurement
- User Story
- Business Project
- Business Project- MOBILITY Study Visits
- Business Project- Recurring PROM Meetings
- 1SP Software Maintenance
- Drupal UAT Checklist
- 1SP Change Requests - mnemonic changes
- Discovery: Validation

#### Card Labels

When making a card, it is important to include the type of work that card is working to fulfill.

There are various labels or tags that should be applied to cards to indicate the type of work. The labels, along with some explanations, are below:

- **Waiting**
  - Dependency on another card.
- **From Post-mortem**
  - Card created from an UNPLANNED card’s post-mortem process.
- **External Dependency**
  - Dependency on external source.
- **DISCOVERY**
  - The “DISCOVERY” process is being done to this card.
- **User Story**
  - A feature that an end-user has requested.
  - There is a specific format for User Stories: "As a *[type of user (or users)]*, I want *[this action]*, so that I *[get this benefit]*"
- **Internal Work**
  - A feature requested from internal users.
- **Change**
  - A small change to something - used mostly as a "papertrail" to keep track of a small change.
- **PoCRI/PROM**
  - Relating to PoCRI/PROM.
- **UNPLANNED**
- **SWARM**
  - Requires that all involved should be working on it – All hands on deck.

#### Assigning Story Points

The format of assigning Story Points follows a Fibonacci sequence. There must not be any 8+ Story Point cards, however. If there are, the card should be split up into subcards until subsequent card reach below eight points.

There must be a clear and unanimous agreement among the card Owner and major contributors for how many Story Points should be assigned to a card.

Generally, the format for assigning story points is within the title of the card at the very beginning with either `XSP` to indicate an unknown number of points or some other agreed upon number like `2SP` for two Story Points.

- `XSP` - Yet to be determined
- `1SP` - 1 Story point

#### Finishing Creation of Card

A Card is considered completed and "Ready for Sprint" once the following have been achieved:

1. There must some *Owner* assigned to the card.
2. There must some *Description* of the problem or desired result from the card.
3. *To-do* lists, contained tasks with appropriately assigned people.
4. Range of *dates* for when the card could be placed into the Sprint board.
5. A clear *Definition of Done* that indicated when a card is completed at the end of a Sprint.
6. Number of *Story Points* needed to complete the Definition of Done (unless it is an UNPLANNED card).

If all requirements are met, the card can be moved into the "Ready for Sprint" column on the "DISCOVERY" board and be advocated for putting into desired Sprint.

### Trello Cards After Sprint

Upon the completion of a Sprint (during the Sprint Planning period), a card will have its Story Points counted. The Story Points will either be adjusted and put back into the next Sprint or written off should the card be finished.

#### Card Story Points Adjustment Syntax

There are various formats that a card's Story Points will go under after the completion of Sprint. They range from the following:

- `1SP (was 1SP, ...)` - 1SP planned this sprint, 1 left over from last sprint.
- `2SP + 1 retro` - Additional 2 story points required and updated after release.
- `1SP (0SP accomplished)` - Card not worked on during sprint.

#### Card Story Points Counting

At the end of a Sprint, all cards present on the Sprint board (minus the "Monitoring" cards) are counted. The cards are counted by the following:

1. Total points released into Sprint.
2. Unplanned points released into Sprint - Total and Achieved.
3. Completed points all in total.
4. Leftover amount of points.

These metrics are then recorded into the "Sprint Summary Card" at the beginning of the Sprint board using this syntax:

[SP Calculation Syntax](https://github.com/splresearch/pocdart_documentation/blob/OOSBg1bz-scrum-documenation/scrum/Sprint_Calculation_Record_Syntax.png?raw=true)

# Glossary

Card
: This refers to a Trello Card. An example card had been created here to understand its parts.

Definition of Done
: A set of requirements that describe what the end product and terminal state of the card to the the Owner and the major contributors.

Discovery
: Time allotted for coming up with a complete set of cards through research, meeting with other members, or other means. Once a card is sufficiently flesh out, the card can then be placed into the "Ready for Sprint" queue on the DISCOVERY board.

Sprint
: A two-week cycle that includes the use of Trello Cards to record work done during that allotted time frame and various meetings to help meet the requirements of said cards.

Owner
: A team member assigned to a Trello card. They are responsible to promoting their card during planning and for facilitating it through the Sprint process.

Story Point
: An arbitrary amount of work that the Owner and major contributors think a card will take to complete.
