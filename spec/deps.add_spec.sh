
Describe 'bldr deps.add'                                                                                           
  Include spec/venv_inc
  setup() {  
    setup_w_bldr
    create_git
  }
  cleanup() {  
    cleanup_dir
  }
  BeforeEach 'setup'
  AfterEach 'cleanup'
                                                                                       
  It 'Creates a .gitmodules files'
    cp $TEST_FILES/dependency.toml ./.bldr/
    cp $TEST_FILES/dependency.lock.toml ./.bldr/ 

    When call bldr deps.add --git  $GIT_CACHE_DIR/bldr-test-dep3.git somedir/dep3
    The output should match pattern '*submodule create somedir/dep3*'
    
    The path .gitmodules should be exist  
    The path somedir/dep3 should be exist
    The path somedir/dep3/README.md should be exist
  End

  It 'Appends the repo name if a folder is given'
    cp $TEST_FILES/dependency.toml ./.bldr/
    cp $TEST_FILES/dependency.lock.toml ./.bldr/ 
    mkdir somedir

    When call bldr deps.add --git  $GIT_CACHE_DIR/bldr-test-dep3.git somedir
    The output should match pattern '*submodule create somedir/bldr-test-dep3*'
    
    The path .gitmodules should be exist  
    The path somedir/bldr-test-dep3 should be exist
    The path somedir/bldr-test-dep3/README.md should be exist
  End

  It 'Puts modules in the correct folder'
    cp $TEST_FILES/dependency.toml ./.bldr/
    cp $TEST_FILES/dependency.lock.toml ./.bldr/ 
    
    When call bldr deps.add --module --git  $GIT_CACHE_DIR/bldr-test-dep3.git
    The output should match pattern '*submodule create .bldr/module/bldr-test-dep3*'
    
    The path .gitmodules should be exist  
    The path .bldr/module/bldr-test-dep3 should be exist
    The path .bldr/module/bldr-test-dep3/README.md should be exist
  End
  
  It 'Renames modules in the correct folder'
    cp $TEST_FILES/dependency.toml ./.bldr/
    cp $TEST_FILES/dependency.lock.toml ./.bldr/ 
    
    When call bldr deps.add --module --git  $GIT_CACHE_DIR/bldr-test-dep3.git test3
    The output should match pattern '*submodule create .bldr/module/test3*'
    
    The path .gitmodules should be exist  
    The path .bldr/module/test3 should be exist
    The path .bldr/module/test3/README.md should be exist
  End
End   