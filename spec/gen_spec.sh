Describe 'bldr gen'                                                                                           
  Include venv/bin/activate
  setup() {  
    setup_w_bldr
    cp -Rf $TEST_FILES/example_generator .bldr/module/
  }
  cleanup() {  
    cleanup_dir
  }
  BeforeEach 'setup'
  AfterEach 'cleanup'
                                                                                       
  It 'Copies the Generators local template folder'

    When call bldr gen example_generator
    The output should match pattern '*Copying*ex_hi.bldr-j2.txt*'
    The output should match pattern '*Copying*ex_hi.bldr-py.txt*'
    The path ./.bldr/history/generated/current/ex_hi.bldr-j2.txt should be exist 
    The path ./.bldr/history/generated/current/ex_hi.bldr-py.txt should be exist                                                                          
    
  End                                                                                                                                                                                                             
End    