Describe 'bldr gen.import'                                                                                           
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
                                                                                       
  It 'Copies all files to Local Template'
    bldr gen.import $TEST_FILES/some_proj

    When call bldr gen.up
    The output should match pattern '*Creating*somefile*'
    The output should match pattern '*Creating*some_deep_file*'
    The path ./somefile should be exist 
    The path ./somedir/some_deep_dir/some_deep_file should be exist                                                                          
    
  End                                                                                                                                                                                                             
End    