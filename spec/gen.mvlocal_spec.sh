Describe 'bldr gen.movelocal'                                                                                           
  Include spec/venv_inc
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
    cp $TEST_FILES/hi.bldr-j2.txt.py ./

    When call bldr gen.mvlocal
    The output should match pattern '*Moving*hi.bldr-j2.txt*'
    The output should match pattern '*Moving*hi.bldr-j2.txt.py*'
    The path ./.bldr/template/hi.bldr-j2.txt should be exist 
    The path ./.bldr/template/hi.bldr-j2.txt.py should be exist                                                                          
    
  End                                                                                                                                                                                                             
End    