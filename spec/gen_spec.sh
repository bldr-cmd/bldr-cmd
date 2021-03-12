Describe 'bldr gen'                                                                                           
  Include venv/bin/activate
  setup() {  
    setup_dir
    bldr init > /dev/null
    cp -Rf $TEST_FILES/example_generator .bldr/module/
  }
  cleanup() {  
    cleanup_dir
  }
  BeforeEach 'setup'
  AfterEach 'cleanup'
                                                                                       
  It 'Copies the Generators local template folder'

    When call bldr gen example_generator
    The output should match pattern '*Creating*ex_hi.bldr-j2.txt*'
    The output should match pattern '*Creating*ex_hi.bldr-py.txt*'
    The path ./.bldr/generated/current/ex_hi.bldr-j2.txt should be exist 
    The path ./.bldr/generated/current/ex_hi.bldr-py.txt should be exist                                                                          
    
  End                                                                                                                                                                                                             
End    