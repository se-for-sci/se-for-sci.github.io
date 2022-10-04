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

Modern tools to promote collective intelligence.

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


Brief history of version control.

![title](CVCS-vs-DVCS.png)

- Local Version Control
    - Mainly just reduced clutter and automated tracking of chronology...

- Centralized Version Control
    - Allows group work on the same files...
    - Single point of failure --- there is only a single "real" repository
    - Backing up is a separate process
    - File locks --- create "race conditions" for commiting changes to that "real" repository
    - What if you lose internet?
    - Branching is cumbersome, so people don't do it (and have trouble reconciling disparate histories when they do)

- Distributed Version Control
    - Resolve most of the above issues...
    - Many separate and independent repos; all are "first-class" citizens
    - Can make commits locally even without internet...
    - ...but can transfer history and information between repositories
    - Branching is lightweight and easy (mainly in Git)


## Investigating history

## Tagging and branching

## Manipulating history

## Collaborative development

## Hooks and configuration
