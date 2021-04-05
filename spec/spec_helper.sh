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
