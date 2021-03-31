
Describe 'bldr deps.get'                                                                                           
  Include venv/bin/activate
  setup() {  
    setup_w_bldr
  }
  cleanup() {  
    cleanup_dir
  }
  BeforeEach 'setup'
  AfterEach 'cleanup'
                                                                                       
  It 'Creates a .gitmodules files'
    cp $TEST_FILES/dependency.toml ./.bldr/
    cp $TEST_FILES/dependency.lock.toml ./.bldr/ 
    git init . > /dev/null
    touch README.md
    git add README.md
    git commit -m "Initial Commit" > /dev/null

    When call bldr deps.get
    The output should match pattern '*render*gitmodules*'
    
    The path .gitmodules should be exist  
    The path somedir/dep1 should be exist
  End

  
End   