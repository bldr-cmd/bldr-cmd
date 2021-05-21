Describe 'bldr init'                                                                                           
  Include spec/venv_inc
  setup() {  
    setup_dir
  }
  cleanup() {  
    cleanup_dir
  }
  BeforeEach 'setup'
  AfterEach 'cleanup'
                                                                                       
  It 'Creates a skeleton .bldr'                                                                                           
    When call bldr init                                                                            
    The output should include 'Initialized the project in'     
    The path ./.bldr/template should be exist                                                       
  End

  It 'Copies Git Hooks'
    create_git

    When call bldr init 
    The path ./.githooks/post-checkout should be exist
    The path ./.githooks/post-rewrite should be exist
    The path ./.git/hooks/post-checkout should be exist
    The path ./.git/hooks/post-rewrite should be exist



    checkpath1()
    {
      if [[ -e ".git/hooks/post-rewrite" || -e ".git\hooks\post-rewrite" ]];
      then
        return 0

      else
        return 1
      fi

    }

    checkpath2()
    {
      if [[ -e ".git/hooks/post-checkout" || -e ".git\hooks\post-checkout" ]];
      then
        return 0
      fi
      return 1
    }
    The result of function checkpath1 should be successful
    The result of function checkpath2 should be successful


  End                                                                                                                                                                                                             
End    