Describe 'bldr gen'                                                                                           
  Include spec/venv_inc
  setup() {  
    setup_w_bldr
    cp -Rf $TEST_FILES/example_generator .bldr/brick/
  }
  cleanup() {  
    cleanup_dir
  }
  BeforeEach 'setup'
  AfterEach 'cleanup'
                                                                                       
  It 'Copies the Generators local template folder'

    When call bldr gen example_generator
    The output should match pattern '*Copying*ex_hi.bldr-j2.txt*'
    The output should match pattern '*Copying*ex_hi.bldr-j2.txt.py*'
    The path ./.bldr/history/generated/current/ex_hi.bldr-j2.txt should be exist 
    The path ./.bldr/history/generated/current/ex_hi.bldr-j2.txt.py should be exist                                                                          
    
  End                                                                                                                                                                                                             
End    