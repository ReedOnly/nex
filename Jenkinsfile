#!/usr/bin/env groovy

pipeline {
    agent none

    stages {
        stage('build') {
            agent { label 'si-build' }
            steps {
                sh """
                    rm -rf libecl

                    PYTHON_VERSION=2.7.13 GCC_VERSION="4.9.4" source /prog/sdpsoft/env.sh
                    root_dir=\$PWD

                    git clone https://github.com/Statoil/libecl.git
                    mkdir libecl/build
                    pushd libecl/build
                    /project/res/x86_64_RH_6/bin/cmake \
                          -DBUILD_SHARED_LIBS=ON \
                          -DCMAKE_CXX_COMPILER=/opt/rh/devtoolset-3/root/usr/bin/g++ \
                          -DCMAKE_INSTALL_PREFIX=\$root_dir/ecl_install \
                          ..
                    make install -j2
                    popd
                    export LD_LIBRARY_PATH="\$root_dir/ecl_install/lib64:\$LD_LIBRARY_PATH"


                    virtualenv venv
                    source venv/bin/activate
                    pip install --upgrade -r requirements.txt

                    mkdir nex_install
                    mkdir build
                    pushd build
                    /project/res/x86_64_RH_6/bin/cmake  \
                            -DCMAKE_INSTALL_PREFIX=\$root_dir/nex_install \
                            -Decl_DIR=\$root_dir/ecl_install/share/cmake/ecl \
                            -DCMAKE_CXX_COMPILER=/opt/rh/devtoolset-3/root/usr/bin/g++ \
                            ..
                    make && make install
                    make test ARGS="-VV"
                    popd
                    deactivate
                   """
                stash name: 'nex-build', includes: 'build/'
                stash name: 'nex', includes: 'nex_install/'
                stash name: 'ecl', includes: 'ecl_install/'
                stash name: 'venv', includes: 'venv/'
            }
            post {
                always {
                    deleteDir()
                }
            }
        }
        stage('test'){
            agent { label 'si-build' }
            steps {
                unstash 'nex'
                unstash 'ecl'
                unstash 'nex-build'
                unstash 'venv'
                sh """
                    PYTHON_VERSION=2.7.13 GCC_VERSION="4.9.4" source /prog/sdpsoft/env.sh
                    root_dir=\$PWD
                    export LD_LIBRARY_PATH="\$root_dir/nex_install/lib:\$root_dir/ecl_install/lib:\$LD_LIBRARY_PATH"
                    source venv/bin/activate
                    pushd build
                    make CTEST_OUTPUT_ON_FAILURE=1 test
                    deactivate
                   """

            }
            post {
                always {
                    deleteDir()
                }
            }
        }
    }
}
