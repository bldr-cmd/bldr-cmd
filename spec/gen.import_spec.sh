Describe 'bldr gen.import'                                                                                           
  Include spec/venv_inc
  setup() {  
    setup_w_bldr gen.import_spec
  }
  cleanup() {  
    cleanup_dir
  }
  BeforeEach 'setup'
  AfterEach 'cleanup'
                                                                                       
  It 'Copies all files to Local Template'
    When call bldr gen.import $TEST_FILES/some_proj
    The output should match pattern '*Creating*somefile*'
    The output should match pattern '*Creating*some_deep_file*'
    The path ./somefile should be exist 
    The path ./somedir/some_deep_dir/some_deep_file should be exist                                                                          
  End       

  It 'Imports to a module named `import.dirname`'
    When call bldr gen.import $TEST_FILES/some_proj
    The path ./.bldr/brick/import.some_proj should be exist
    The output should match pattern '*Copying templates *import*some_proj*template*'
  End

  It 'Converts files to templates'
    When call bldr gen.import $TEST_FILES/some_proj
    The path ./.bldr/config/config.toml should be exist
    The path ./.bldr/brick/import.some_proj/template/net_code.bldr-j2.cs should be exist

    The path ./.bldr/brick/import.some_proj/template/net_code.bldr-j2.cs contents should include "TheNewModule"
    The path ./.bldr/brick/import.some_proj/template/net_code.bldr-j2.cs contents should include "ANotSoSimilarModule"
    The path ./.bldr/brick/import.some_proj/template/net_code.bldr-j2.cs contents should include "ANew.Nested.OtherPlace.Function()"
    The output should match pattern '*Generating *import.some_proj*template*net_code.bldr-j2.cs*'
    
    #cat ./.bldr/module/import.some_proj/template/net_code.bldr-j2.cs
    #echo "gen.up\n"
    
    The path ./net_code.cs contents should include "MyNewPlugableModule.CoolFunction(1,2,3)"
    
    #cat ./net_code.cs
    #The output should match pattern '*Copying local *import.some_proj/template*'
  End   
  It 'Imports project as a template with --as-template'
    When call bldr gen.import --as-template $TEST_FILES/some_proj
    
    The path ./template/net_code.bldr-j2.cs should be exist


    
    The output should match pattern '*Generating *template*net_code.bldr-j2.cs*'
    
  End

  It 'Ignores files marked in the exclude_globs'
    When call bldr gen.import --as-template $TEST_FILES/some_proj
    
    The path ./template/net_code.bldr-j2.cs should be exist
    The path ./template/project.sln should not be exist

    The output should match pattern '*Skipping File *project.sln*'
    
  End

  It 'Places the import at the destination path'
    When call bldr gen.import --path different/nested/name $TEST_FILES/some_proj
    The path .bldr/brick/import.some_proj/template/different/nested/name/somefile should be exist

    The output should match pattern '*different*nested*name*'
  End

  It 'Renames files'
    When call bldr gen.import --as-template $TEST_FILES/some_proj
    The path ./template/RightName.md should be exist
    The output should match pattern '*template*RightName.md*'

  End

  It 'Replaces text in files'
    When call bldr gen.import $TEST_FILES/some_proj
    The path ./README.md should be exist

    The path ./README.md contents should include "DE Designworks"
    The output should match pattern '*Generating *template*README.md*'
  End     
End    