Describe 'bldr gen.up'                                                                                           
  Include venv/bin/activate
  setup() {  
    rm -Rf _test_temp
    mkdir -p _test_temp
    cd _test_temp
    bldr init
  }
  cleanup() {  
    cd ..
    rm -Rf _test_temp
  }
  BeforeEach 'setup'
  AfterEach 'cleanup'
                                                                                       
  # It ''                                                                                           
  #   When call bldr                                                                              
  #   The output should equal 'Hello shellspec!'                                                              
  # End                                                                                                                                                                                                             
End   