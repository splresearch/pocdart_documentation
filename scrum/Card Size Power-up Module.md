# Purpose

The [card size power-up module](https://trello.com/b/mPW9C7y6/sprint-now/power-up/5cd476e1efce1d2e0cbe53a8) was installed onto both the "SPRINT-now" board and the "READY FOR SPRINT" section in the "DISCOVERY" board.

The purpose of installing the power-up is to help with the calculation of how many cards are in various columns on a Trello board and seeing how many points of work are allocated to a particular assignee and label.

Another future purpose is combining this module with another one that can access the card size of cards and make charts and dashboard.

# Required by

End-of-Sprint calculations

(In the future) [Dashboards by Screenful power-up module](https://trello.com/b/mPW9C7y6/sprint-now/power-up/570262ea1100fa611d7e200a)

# Maintenance Requirements

There are a few problems currently that should be kept in mind when working with this module.

Because there are only three buckets to determine the size of a card, there is no built-in way to keep track of retro points for a given card. To help alleviate this issue, should a card be recycled another Sprint - a custom field named "Total" should be created. Inside of that field, the total amount of Story Points allocated to the life of a given card should be stored.

# Configuration

In the "Card Size" settings located above the Trello card columns, there are a few options that have been selected.

On the 'front' of a card, the card size (total amount of points that the card is worth) and the remaining points will be shown with orange and blue boxes respectively.
On the 'back' of a card, the card size (total amount of points that the card is worth), the number of points already spent on the card, and the remaining points will be shown with orange, green, and blue boxes respectively.
In addition to those settings, this is also where you will find the total point count by either column, assignee, or label based on each card's size.
