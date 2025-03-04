This goes over what parts fall back to git and what parts need other implementation
Let's go over all the functions

# not git
## fork [ --no-history ]
Permit users to have superset/subset groups 

## invite [ email ]
Invite someone to the particular 

## login
Set your credentials

## reject [ ident ]
Reject an invite

## request [ ident ]
Request to be part of a team
risk: there's spamming that needs to be prevented

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

## checkout - switch
change within the project between different credentials such as staging/production

## config 
Config controls:

 * Where the default server is for projects
 * encryption method

## init
## log
## pull
## fetch
## merge
## push
## commit
