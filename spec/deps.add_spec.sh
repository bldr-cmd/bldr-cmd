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

  It 'Puts bricks in the correct folder'
    cp $TEST_FILES/dependency.toml ./.bldr/
    cp $TEST_FILES/dependency.lock.toml ./.bldr/ 
    
    When call bldr deps.add --brick --git  $GIT_CACHE_DIR/bldr-test-dep3.git
    The output should match pattern '*submodule create .bldr/brick/bldr-test-dep3*'
    
    The path .gitmodules should be exist  
    The path .bldr/brick/bldr-test-dep3 should be exist
    The path .bldr/brick/bldr-test-dep3/README.md should be exist
  End
  
  It 'Renames bricks in the correct folder'
    cp $TEST_FILES/dependency.toml ./.bldr/
    cp $TEST_FILES/dependency.lock.toml ./.bldr/ 
    
    When call bldr deps.add --brick --git  $GIT_CACHE_DIR/bldr-test-dep3.git test3
    The output should match pattern '*submodule create .bldr/brick/test3*'
    
    The path .gitmodules should be exist  
    The path .bldr/brick/test3 should be exist
    The path .bldr/brick/test3/README.md should be exist
  End

  It 'Can add locally stored git repositories'
    deps_add_file_constructor > /dev/null 2>&1
    When call cd foo
    The path ./file.txt should be exist
    The path ./stuff.txt should not be exist
    cd ..
    The path ./dep should not be exist
  End

  It 'Can add symbolic links of directories'
    add_link_setup > /dev/null 2>&1
    When call bldr deps.add .././test2 ./f1/././f2/haha -l > /dev/null 2>&1
    The output should match pattern '*Getting Dependencies*'
    The path ./f1/f2/haha should be exist
    The path ./f1/f2/haha/newFile.txt should be exist
    The path ./f1/f2/haha/subFolder should be exist
    The path ./f1/f2/haha/subFolder/newnewFile.txt should be exist
    The path ./f1/oldoldFile.txt should be exist
    The path ./f1/f2/oldoldoldFile.txt should be exist
    The path ./f1/f2/test2 should not be exist
    The path ./f1/test2 should not be exist
    The path ./test2 should not be exist


  End

  

End   