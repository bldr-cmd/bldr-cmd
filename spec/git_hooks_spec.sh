
Describe 'git checkout'                                                                                           
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
                                                                                       
  It 'Creates git submodules and fetches them'
    generate_test_dep_sys
    
    When call git checkout A
    The path child1/filea.txt should be exist  
    The path child1/fileb.txt should not be exist  

    The path child2/filea.txt should be exist  
    The path child2/fileb.txt should not be exist  


    When call git checkout B

    The path child1/fileb.txt should be exist  
    The path child1/filea.txt should not be exist  

    The path child2/fileb.txt should be exist  
    The path child2/filea.txt should not be exist  




  End

  
End   