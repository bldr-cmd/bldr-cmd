# shellcheck shell=bash

# Defining variables and functions here will affect all specfiles.
# Change shell options inside a function may cause different behavior,
# so it is better to set them here.
# set -eu

if [ -e venv/bin/activate ]; then
    source venv/bin/activate
fi

if [ -e venv/Scripts/activate ]; then
    source venv/Scripts/activate
fi

export GIT_CACHE_DIR=$SHELLSPEC_PROJECT_ROOT/spec/cache
export TEST_FILES=$SHELLSPEC_PROJECT_ROOT/spec/files
export BLDR_VERBOSE=1
# This callback function will be invoked only once before loading specfiles.
spec_helper_precheck() {
  # Available functions: info, warn, error, abort, setenv, unsetenv
  # Available variables: VERSION, SHELL_TYPE, SHELL_VERSION
  
  [ ! -d "$GIT_CACHE_DIR/brk-dotnet-serial-sim.git" ] && git clone --mirror git@svn.daveengineering.com:bldr/brk-dotnet-serial-sim.git $GIT_CACHE_DIR/brk-dotnet-serial-sim.git
  [ ! -d "$GIT_CACHE_DIR/bldr-test-dep1.git" ] && git clone --mirror git@svn.daveengineering.com:bldr/bldr-test-dep1.git $GIT_CACHE_DIR/bldr-test-dep1.git
  [ ! -d "$GIT_CACHE_DIR/bldr-test-dep3.git" ] && git clone --mirror git@svn.daveengineering.com:bldr/bldr-test-dep3.git $GIT_CACHE_DIR/bldr-test-dep3.git
  [ ! -d "$GIT_CACHE_DIR/child1" ] && create_child1
  [ ! -d "$GIT_CACHE_DIR/child2" ] && create_child2
  [ ! -d "$GIT_CACHE_DIR/parent" ] && create_parent

  : minimum_version "0.28.1"
}

# This callback function will be invoked after a specfile has been loaded.
spec_helper_loaded() {
  :
}

# This callback function will be invoked after core modules has been loaded.
spec_helper_configure() {
  # Available functions: import, before_each, after_each, before_all, after_all
  : import 'support/custom_matcher'
}

# Create/delete the scratch directory
setup_dir() {  
    cd $SHELLSPEC_PROJECT_ROOT
    rm -Rf _test_temp
    mkdir -p _test_temp
    cd _test_temp
    
}
setup_w_bldr() {
  setup_dir
  bldr init > /dev/null
  if [ "$#" -eq 1 ]; then
    cp -Rf $TEST_FILES/$1/* ./ 2>/dev/null || :
    cp -Rf $TEST_FILES/$1/.* ./ 2>/dev/null || :
  fi
}
cleanup_dir() {  
    cd $SHELLSPEC_PROJECT_ROOT
    rm -Rf _test_temp
    
}

create_git() {
    git init . > /dev/null
    touch README.md
    git add README.md
    git commit -m "Initial Commit" > /dev/null
}

create_child1()
{
  mkdir -p $GIT_CACHE_DIR/child1
  cd $GIT_CACHE_DIR/child1

  create_child
  return 0
}

create_child2()
{
  mkdir -p $GIT_CACHE_DIR/child2
  cd $GIT_CACHE_DIR/child2

  create_child
  return 0
}

create_child()
{
  git init
  git checkout -b A
  echo "a" >> filea.txt
  git add .
  git commit -m "made A"

  git checkout -b B
  echo "b" >> fileb.txt
  rm filea.txt
  git add .
  git commit -m "made B"
}

create_parent()
{
  mkdir -p $GIT_CACHE_DIR/parent
  cd $GIT_CACHE_DIR/parent

  git init
  echo "empty" >> file.txt
  bldr init
  bldr deps.get
  git add .
  git commit -m "start master"

  # Make branch A
  git checkout -b A
  echo "a" >> filea.txt
  git add .
  git commit -m "made A"
  bldr deps.add ../child1 . -b A
  git add . 
  git commit -m "done with parent A"

  bldr deps.get
  git add .
  git commit -m "Save Lockfile"

  # Make file B
  git checkout -b B
  echo "b" >> fileb.txt
  rm filea.txt
  git add .
  git commit -m "made B"
  bldr deps.add ../child2 . -b B
  cd child1
  git checkout B
  cd ..

  git add .
  git commit -m "done with parent B"

  bldr deps.get
  git add .
  git commit -m "Save Lockfile"
  return 0
}

generate_test_dep_sys()
{
  git clone file://$GIT_CACHE_DIR/parent
  cd parent
  git checkout A
  
  bldr deps.get
}

deps_add_file_constructor()
{
  mkdir dep
  mkdir main
  cd dep
  echo "hi" > file.txt
  git init
  git add .
  git commit -m "file added"
  cd ..
  cd main
  git init
  echo "bye" > stuff.txt
  git add .
  git commit -m "yaya"
  bldr init
  bldr deps.add file://../dep foo 

}

add_link_setup()
{
  mkdir test1
  mkdir test2
  cd test2
  echo "alsdjkas" > newFile.txt
  mkdir subFolder
  cd subFolder
  echo "askdhad" > newnewFile.txt
  cd ../../test1
  echo "alsdjkas" > oldFile.txt
  mkdir f1
  cd f1
  echo "alsdjkas" > oldoldFile.txt
  mkdir f2
  cd f2
  echo "alsdjkas" > oldoldoldFile.txt
  cd ../..
  git init
  git add .
  git commit -m "sndkas"
}