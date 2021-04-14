Describe 'bldr init'                                                                                           
  Include venv/bin/activate
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

    The output should include '.git/hooks/post-rewrite'
    The output should include '.git/hooks/post-checkout'
  End                                                                                                                                                                                                             
End    