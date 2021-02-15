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
                                                                                       
  It 'Supports inline templates'
    echo "hello World\n" > hi.bldr-j2.txt                                                                                           
    When call bldr gen.up
    The output should match pattern '*Creating*hi.txt*'

    The path hi.txt should be exist  
    The path hi.txt contents should include "hello World"                                                          
  End                                                                                                                                                                                                             
End   