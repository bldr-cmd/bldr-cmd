
Describe 'bldr gen.up'
  Include spec/venv_inc
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
    cp $TEST_FILES/hi.bldr-j2.txt.py ./

    When call bldr gen.up
    The output should match pattern '*Creating*hi.txt*'

    The path hi.txt should be exist
    The path hi.txt contents should include "hellow"
  End

  It 'Supports Python templates'
    cp $TEST_FILES/bare.bldr-py.txt ./

    When call bldr gen.up
    The output should match pattern '*Creating*bare.txt*'

    The path bare.txt should be exist
    The path bare.txt contents should include "This is a bare python template"
  End

  It 'Templates Only Apply Changes'
    cp $TEST_FILES/hi.bldr-j2.txt ./
    cp $TEST_FILES/hi.bldr-j2.txt.py ./

    bldr gen.up > /dev/null
    echo -e "NO" >> hi.txt
    sed -i 's/Lets/Lets NOT/g' hi.bldr-j2.txt

    When call bldr gen.up
    The output should match pattern '*Updating*hi.txt*'

    The path hi.txt should be exist
    The path hi.txt contents should include "NO"
    The path hi.txt contents should include "Lets NOT"
  End

  It 'Has a Default Local Template In .bldr/template'
    mkdir -p ./.bldr/template/
    cp $TEST_FILES/hi.bldr-j2.txt ./.bldr/template/
    cp $TEST_FILES/hi.bldr-j2.txt.py ./.bldr/template/

    When call bldr gen.up
    The output should match pattern '*Creating*hi.txt*'

    The path hi.txt should be exist
    The path hi.txt contents should include "hellow"
    The path hi.txt.py should not be exist
  End

  It 'Removes deleted files'
    mkdir -p ./.bldr/template/
    cp $TEST_FILES/hi.bldr-j2.txt ./.bldr/template/
    cp $TEST_FILES/hi.bldr-j2.txt.py ./.bldr/template/
    cp $TEST_FILES/hi.bldr-j2.txt ./.bldr/template/bye.bldr-j2.txt
    cp $TEST_FILES/hi.bldr-j2.txt.py ./.bldr/template/bye.bldr-j2.txt.py
    bldr gen.up > /dev/null

    rm ./.bldr/template/bye.bldr-j2.txt
    rm ./.bldr/template/bye.bldr-j2.txt.py

    When call bldr gen.up
    The output should match pattern '*Deleting*bye.txt*'

    The path bye.txt should not be exist
  End

  It 'Removes deleted files from removed directories'
    mkdir -p ./.bldr/template/somedir/somedir2
    cp $TEST_FILES/hi.bldr-j2.txt ./.bldr/template/
    cp $TEST_FILES/hi.bldr-j2.txt.py ./.bldr/template/
    cp $TEST_FILES/hi.bldr-j2.txt ./.bldr/template/somedir/somedir2/bye.bldr-j2.txt
    cp $TEST_FILES/hi.bldr-j2.txt.py ./.bldr/template/somedir/somedir2/bye.bldr-j2.txt.py
    bldr gen.up > /dev/null

    rm -Rf ./.bldr/template/somedir
    
    When call bldr gen.up
    The output should match pattern '*Deleting*bye.txt*'

    The path somedir/somedir2/bye.txt should not be exist
    The path somedir should not be exist
  End

  It 'Reruns generators'
    create_git
    bldr deps.add --brick --git $GIT_CACHE_DIR/brk-dotnet-serial-sim.git > /dev/null
    bldr gen brk-dotnet-serial-sim > /dev/null
    bldr gen.up > /dev/null

    When call bldr gen.up

    The output should match pattern '*Copying*SerialSimulator.bldr-j2.cs*'

    The path SerialSimulator/SerialSimulator.cs should be exist
  End  
End