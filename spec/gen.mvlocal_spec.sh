Describe 'bldr gen.movelocal'                                                                                           
  Include venv/bin/activate
  setup() {  
    setup_w_bldr
  }
  cleanup() {  
    cleanup_dir
  }
  BeforeEach 'setup'
  AfterEach 'cleanup'
                                                                                       
  It 'Saves Inline Template to Local Template'
    cp $TEST_FILES/hi.bldr-j2.txt ./
    cp $TEST_FILES/hi.bldr-py.txt ./

    When call bldr gen.mvlocal
    The output should match pattern '*Moving*hi.bldr-j2.txt*'
    The output should match pattern '*Moving*hi.bldr-py.txt*'
    The path ./.bldr/local/hi.bldr-j2.txt should be exist 
    The path ./.bldr/local/hi.bldr-py.txt should be exist                                                                          
    
  End                                                                                                                                                                                                             
End    