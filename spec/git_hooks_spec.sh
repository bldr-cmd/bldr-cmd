
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
                                                                                       
  It 'Creates git submodules and fetches them #1'
    generate_test_dep_sys > /dev/null 2>&1
    git checkout B > /dev/null 2>&1
    
    When call git checkout A
    The output should match pattern "*"

    The path child1/filea.txt should be exist
    The path child1/fileb.txt should not be exist
    The path child2 should not be exist
  End


  It 'Creates git submodules and fetches them #1'
    generate_test_dep_sys > /dev/null 2>&1

    git checkout A > /dev/null 2>&1
    When call git checkout B
    The output should match pattern "*"
    
    The path child2/fileb.txt should be exist
    The path child2/filea.txt should not be exist
    The path child1/fileb.txt should be exist
    The path child1/filea.txt should not be exist

  End

  
End   