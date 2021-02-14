
setup_dir() {  
    rm -Rf _test_temp
    mkdir -p _test_temp
    cd _test_temp
}
cleanup_dir() {  
    cd ..
    rm -Rf _test_temp
}