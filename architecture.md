# Notes & Introduction

This goes over what parts fall back to git and what parts need other implementation
Let's go over all the functions

# not git
## fork [ --no-history ]
Permit users to have superset/subset groups 

## invite [ email ]
Invite someone to the particular 

## login
Set your credentials
These should be handled like git

## reject [ ident ]
Reject an invite
This is recorded somewhere

## request [ ident ]
Request to be part of a team
risk: there's spamming that needs to be prevented
This is recorded somewhere

## members (should have an alias to request(s) and invite(s))
Have a list of current members / invites

# git-like but not actually git 
## add
Put a new secret. This is a triplet:
  description, resolvable path, credential

 * description is needed as meta-information to keep identify the thing being added.

   1. It should support namespacing so people can be like

       * aws/project id
       * aws/secret

   1. The delimeter (:, / or .) should be flexible. Someone shouldn't have to read
      documentation or have to remember it. If this proves to be hostile instead of
      friendly, settle on /

   1. It should be case insensitive

   1. Spacing should be allowed to be friendly 

 * resolvable path is needed because not all project secrets go in the same place 
   and, importantly, some can exist out of tree.

   Having relative paths "..", expandable and variable resolvable (~, $HOME) are
   crucial.

   Replacement versus appending is also needed. Making this explicit can be confusing.
   This is also not completely derivable by extension as .ini could be both, .toml 
   could be both. Furthermore, things like .toml and scopable ini can be complicated
   and not specifiable on a single line without inventing syntax.

   Some kind of dumb schema is needed but not the kind that like hashicorp vault or 
   other complicated solutions use.

 * credential is needed for obvious reasons.

There could be an fzf-like interface where you can query for description. In this
approach, schemas are kept in some wiki style database and the user can just type in
what the credential is. An embeddings database or some small network can exist to
resolve it.

If it is a new one, the entire process can be tui friendly.


       [ new description ] -> [ type in path ] -> 
       [ (optional) example ] -> template

Templates can do replace/append/whole file or whatever implicitly. 
Essentially you're avoiding collisions. There's the following formats:

* Unscoped:
    * k/v flat list
* Scoped:
    * json
    * toml
    * ini
    * yaml

Essentially $EDITOR pops up with a comment:

```
# These lines are ignored
# Just provide the stanza for the credential in proper format. 
#
# We've given you something to work with. 
# It's probably wrong and only meant as an example
#
{
      "password": {secret}
}
```
If the user provides an example file then we tell them to replace the secret
with {secret}
Alternatively there could be an option to give an example credential file
and derive the format from that.

# actually git 
This is a fancy tricked out repo with git hooks

The flow is debatable. The git workflow has two ways to start
 * init - set up empty scaffolding
 * clone - get existing data and scaffloding 

"Easier" here is two possibilities:

 * closer to git workflow
 * conceptually less abstract

So there is the assumption the person is already familiar with the git workflow
This entire system is "git but also, not git"

The confusion in a product is from 
 * when it presents itself as taking responsibility that it doesn't or
 * suggesting a mode of operation that isn't correct. 

For instance, I was dealing with MCP. I thought it could be used as an interceptor in the regular agentic flow as opposed to a tool calling mechanism.

This was both. I was looking for a way to call it *as part of the flow* like a proxy and being perplexed why there was no documentation on it. LLMs were confused as well (but that's to be expected).

These are solved by presentation, communication, and design. Introducing new porcelein comamnds can be taken as weighty ... potentially heavy concepts with confusing consequences. We need to avoid that.

## checkout - switch
change within the project between different credentials such as staging/production

## config 
Config controls:

 * Where the default server is for projects
 * encryption method - this should default to ~/.ssh/id_(whatever)

## init
## log
## pull
## fetch
## merge
## push
## commit

### Auto-secret rewriter

So this is a git hook that prevents secrets from going up as a built-in linter. But it Does Not scold the user instead it does something like this:

    + Checking commit
    |
    X You included a secret, probably. Here's the line:
    | 
    | db = db.connect(server, key=123123123123)
    |
    +- Here's a few options --
       ( nblx the key )
       ( this isn't a secret / I don't care! Add # nblx-go-away to the line )

First one needs a demo

    + nblxing the key, here's a suggested name.
    | Feel free to edit it or press enter to accept.
    | Clear it out to abort
    | 
    | [ DB_SERVER            ]
    | 
    + Ok Here's the code now:
    | db = db.connect(server, key=DB_SERVER)
    |
    | ( continue with commit )
    | ( abort all of this    )
    +

On abort:

    + No problem. You can make these warnings never appear
    | with one of the following:
    |
    | git config nblx.block_commit=no
    |
    + this will just edit the local configuration
    | just do that with a -g option to never get blocked
    |
    | Notes: 
    |
    | * I'll still warn you, you can just ignore them.  
    |
    | * This isn't a convenience option. You should only
    |   use it if nblx is really broken
    +-

