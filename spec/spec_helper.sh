# shellcheck shell=sh

# Defining variables and functions here will affect all specfiles.
# Change shell options inside a function may cause different behavior,
# so it is better to set them here.
# set -eu

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
    cd ..
    rm -Rf _test_temp
}

create_git() {
    git init . > /dev/null
    touch README.md
    git add README.md
    git commit -m "Initial Commit" > /dev/null
}


generate_test_dep_sys()
{
  # makes 3 git repos, par, child, child
  # parent has two submodules, the childs
  # parent has test ver of dependencies.lock.toml and dependencies.toml

  mkdir parent
  mkdir child1
  mkdir child2

  #
  # make master parent
  #
  cd parent
  git init
  echo "empty" >> file.txt
  bldr init
  bldr deps.get
  git add .
  git commit -m "start master"

  #make file a
  git checkout -b A
  echo "a" >> filea.txt
  git add .
  git commit -m "made A"

  #make file b
  git checkout -b B
  echo "b" >> fileb.txt
  rm filea.txt
  git add .
  git commit -m "made B"

  #
  # make child1
  # 
  cd ..
  cd child1
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

  #
  # make child2
  #
  cd ..
  cd child2
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
  cd ..

  echo "Running bldr"
  cd parent
  bldr init
  bldr deps.get
  git add .
  git commit -m "done with parent A"


  git checkout A
  bldr deps.add ../child1 . -b A

  git add .
  git commit -m "done with parent A"

  git checkout B
  bldr init
  bldr deps.get
  bldr deps.add ../child2 . -b B
  bldr init
  bldr deps.get
  git add .
  git commit -m "done with parent A"


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
