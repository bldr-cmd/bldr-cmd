Describe 'bldr init'                                                                                           
  Include venv/bin/activate
  setup() {  
    rm -Rf _test_temp
    mkdir -p _test_temp
    cd _test_temp
  }
  cleanup() {  
    cd ..
    rm -Rf _test_temp
  }
  BeforeEach 'setup'
  AfterEach 'cleanup'
                                                                                       
  It 'Creates a skeleton .bldr'                                                                                           
    When call bldr init                                                                            
    The output should include 'Initialized the repository in'                                                              
  End                                                                                                                                                                                                             
End    