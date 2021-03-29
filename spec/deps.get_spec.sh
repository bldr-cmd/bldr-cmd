
Describe 'bldr deps.get'                                                                                           
  Include venv/bin/activate
  setup() {  
    setup_dir
    bldr init > /dev/null
  }
  cleanup() {  
    cleanup_dir
  }
  BeforeEach 'setup'
  AfterEach 'cleanup'
                                                                                       
  It 'Creates a .gitmodules files'                                                                                           
    When call bldr deps.get
    The output should match pattern '*render*gitmodules*'
    
    The path .gitmodules should be exist  
  End

  
End   