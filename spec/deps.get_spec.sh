
Describe 'bldr deps.get'                                                                                           
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
                                                                                       
  It 'Creates git submodules and fetches them'
    cp $TEST_FILES/dependency.toml ./.bldr/
    cp $TEST_FILES/dependency.lock.toml ./.bldr/ 

    When call bldr deps.get
    The output should match pattern '*submodule create somedir*dep1*'
    
    The path .gitmodules should be exist  
    The path somedir/dep1 should be exist
  End

  
End   