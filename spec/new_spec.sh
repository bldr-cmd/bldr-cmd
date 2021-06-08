
Describe 'bldr new'                                                                                           
  Include spec/venv_inc
  setup() {  
    setup_w_bldr
    create_git
  }
  cleanup() {  
    cleanup_dir
  }
  

  BeforeEach 'setup'
  AfterEach 'cleanup'
                                                                                       
  It 'Calls bldr new, should add dependency'
    git init > /dev/null 2>&1
    When call bldr new https://github.com/microsoft/playwright-test > /dev/null 2>&1
    The output should match pattern '*Checking Migrations*'

    The path ./playwright-test/ should be exist
  End
End   