Describe 'bldr gen.import'                                                                                           
  Include venv/bin/activate
  setup() {  
    setup_w_bldr
  }
  cleanup() {  
    cleanup_dir
  }
  BeforeEach 'setup'
  AfterEach 'cleanup'
                                                                                       
  It 'Copies all files to Local Template'
    bldr gen.import $TEST_FILES/some_proj > /dev/null

    When call bldr gen.up
    The output should match pattern '*Creating*somefile*'
    The output should match pattern '*Creating*some_deep_file*'
    The path ./somefile should be exist 
    The path ./somedir/some_deep_dir/some_deep_file should be exist                                                                          
    
  End       

  It 'Warns to run `bldr gen.up`'
    When call bldr gen.import $TEST_FILES/some_proj
    The output should match pattern '*Import Complete.  Run `bldr gen.up` to update files*'
  End 

  It 'Imports to a module named `import.dirname`'
    When call bldr gen.import $TEST_FILES/some_proj
    The path ./.bldr/module/import.some_proj should be exist
    The output should match pattern '*Copying local *import.some_proj/local*'
  End                                                                                                                                                                                                            
End    