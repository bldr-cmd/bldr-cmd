Describe 'bldr init'                                                                                           
  Include venv/bin/activate
  setup() {  
    setup_dir
  }
  cleanup() {  
    cleanup_dir
  }
  BeforeEach 'setup'
  AfterEach 'cleanup'
                                                                                       
  It 'Creates a skeleton .bldr'                                                                                           
    When call bldr init                                                                            
    The output should include 'Initialized the repository in'                                                              
  End                                                                                                                                                                                                             
End    