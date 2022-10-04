# Version Control

## Intro to git

Good practice in programming project management requires a version control system. 

Old school techniques are usually bad.

- Version filenames is a disaster. 
    - mythesis_v1.tex, mythesis_v2.tex, mythesis_last_v3.tex
    - create clutter
    - Filenames rarely contain information other than chronology
    - Parallel independent changes super hard to keep track of
    - Did you finally notice a problem in v119 that has been around for a while, but you have no idea where the error was introduced?

- Sharing files with others is a disaster. 
    - Emailing files sucks --- only magnifies the problems above
    - Track changes feature Google Docs or Word --- not so useful for anything complex

- Disaster recover is a disaster. 
    - Oh F#@K! Did I just overwrite all my work from last night??!!!?

![title](phd101212s.png)

Modern version control techniques are usually great.

Modern tools for collective intelligence.

- Automated history of everything 
       - not just files, but whole projects with folders and subfolders 
       - who, what, when, and (most important) why

- Automated sharing of everyone's latest edits
        - no more emailing files around

- Easier disaster recovery with distributed VCSes like Git or Mercurial (see later)

- Support for automated testing (we'll cover this in future lectures)

- Infinite sandboxes for clutter-free, fear-free experimentation
        - this is where Git especially shines -- main topic today

- CAVEAT 1: All of this works best with plain text files

- CAVEAT 2: All of this works best with a highly modular file structure

- The git feedback effect: 
        - Using git encourages positive changes to your workflow. 
        - And making your workflow more git-friendly will make your work better overall.


A bit of history.

### Centralized Version Control


## Investigating history

## Tagging and branching

## Manipulating history

## Collaborative development

## Hooks and configuration
