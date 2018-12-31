## App Deploy to Heroku
I wasn't able to deploy my application on heroku.
I tried to deploy my application(my-app) using conda-buildpack[https://github.com/conda/conda-buildpack](https://github.com/conda/conda-buildpack) for slug size over(300 MB), but result in following many times:

```bash
Counting objects: 80, done.
Delta compression using up to 4 threads.
Compressing objects: 100% (70/70), done.
Writing objects: 100% (80/80), 1.19 MiB | 85.00 KiB/s, done.
Total 80 (delta 15), reused 0 (delta 0)
remote: Compressing source files... done.
remote: Building source:
remote:
remote: -----> Python/Conda app detected
remote: -----> Preparing Python/Miniconda Environment (3.8.3)
remote: /app/tmp/buildpacks/2abac4b7166986c6b1b33fcacccb13fb4e2036a9358f31ed8886bbf37c9987c7fbb8243090f0438ebbf02852a1cbeb1b5cae47f67dc2670115ce6d7bd2468300/bin/steps/conda_compile: line 9: conda: command not found
remote:  !     Push rejected, failed to compile Python/Conda app.
remote:
remote:  !     Push failed
remote: Verifying deploy...
remote:
remote: !       Push rejected to twistats.
remote:
To https://git.heroku.com/twistats.git
 ! [remote rejected] master -> master (pre-receive hook declined)
error: failed to push some refs to 'https://git.heroku.com/twistats.git'

# twistats is my application name
```

On dashboard log in heroku webpage(myapp > Overview > Latest activity ), it was written as follows:

```bash
-----> Python/Conda app detected
-----> Preparing Python/Miniconda Environment (3.8.3)
/app/tmp/buildpacks/2abac4b7166986c6b1b33fcacccb13fb4e2036a9358f31ed8886bbf37c9987c7fbb8243090f0438ebbf02852a1cbeb1b5cae47f67dc2670115ce6d7bd2468300/bin/steps/conda_compile: line 9: conda: command not found
 !     Push rejected, failed to compile Python/Conda app.
 !     Push failed
```

## condaのコマンドがないことが原因なのでは？
