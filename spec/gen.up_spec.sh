
Describe 'bldr gen.up'                                                                                           
  Include venv/bin/activate
  setup() {  
    setup_w_bldr
  }
  cleanup() {  
    cleanup_dir
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

  It 'Supports Jinja2 templates'
    cp $TEST_FILES/hi.bldr-j2.txt ./
    cp $TEST_FILES/hi.bldr-py.txt ./

    When call bldr gen.up
    The output should match pattern '*Creating*hi.txt*'

    The path hi.txt should be exist  
    The path hi.txt contents should include "hellow"                                                          
  End  

  It 'Templates Only Apply Changes'
    cp $TEST_FILES/hi.bldr-j2.txt ./
    cp $TEST_FILES/hi.bldr-py.txt ./

    bldr gen.up > /dev/null
    echo -e "NO" >> hi.txt
    sed -i 's/Lets/Lets NOT/g' hi.bldr-j2.txt

    When call bldr gen.up
    The output should match pattern '*Updating*hi.txt*'

    The path hi.txt should be exist  
    The path hi.txt contents should include "NO"   
    The path hi.txt contents should include "Lets NOT"                                                         
  End  

  It 'Has a Default Local Template In .bldr/local'
    mkdir -p ./.bldr/local/
    cp $TEST_FILES/hi.bldr-j2.txt ./.bldr/local/
    cp $TEST_FILES/hi.bldr-py.txt ./.bldr/local/

    When call bldr gen.up
    The output should match pattern '*Creating*hi.txt*'

    The path hi.txt should be exist  
    The path hi.txt contents should include "hellow"                                                          
  End
End   