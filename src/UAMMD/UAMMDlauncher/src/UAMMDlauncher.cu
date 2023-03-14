#include "UAMMDstructured.cuh"

using namespace uammd::structured;

int main(int argc, char *argv[]) {

    if (argc < 2) {
        uammd::System::log<uammd::System::CRITICAL>("No input file provided!");
        return EXIT_FAILURE;
    }

    startSelfStartingSimulation(argv[1]);

    return EXIT_SUCCESS;
}
