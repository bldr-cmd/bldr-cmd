
Describe 'bldr deps.get'                                                                                           
  Include venv/bin/activate
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

    When call bldr deps.add --git git@svn.daveengineering.com:bldr/bldr-test-dep3.git somedir/dep3
    The output should match pattern '*submodule create somedir/dep3*'
    
    The path .gitmodules should be exist  
    The path somedir/dep3 should be exist
    The path somedir/dep3/README.md should be exist
  End

  
End   