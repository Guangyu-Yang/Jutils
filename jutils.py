from pathlib import Path
import sys, argparse

from convert_results_utils import convert_leafcutter_results, convert_rmats_results, convert_mntjulip_results
from venn_diagram_utils import plot_venn_diagram
from heatmap_utils import plot_heatmap


def get_arguments():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(help='commands', dest="command")

    r_parser = subparser.add_parser('convert-results')
    r_parser.add_argument('--leafcutter-dir', type=str, help='The directory contains the leafcutter_ds_cluster_significance.txt, leafcutter_ds_effect_sizes.txt and *.counts.gz')
    r_parser.add_argument('--rmat-dir', type=str, help='The directory contains the *.ReadsOnTargetAndJunctionCounts.txt and *.JunctionCountOnly.txt.')
    r_parser.add_argument('--mntjulip-dir', type=str, help='The directory contains diff_spliced_introns.txt, diff_spliced_groups.txt, diff_introns.txt and intron_data.txt')
    r_parser.add_argument('--out-dir', type=str, default='./out', help='The output directory')

    v_parser = subparser.add_parser('venn-diagram', help='')
    v_parser.add_argument('--tsv-file-list', type=str, help='A file that contains path of tsv files')
    v_parser.add_argument('--p-value', type=float, default=0.05, help='Provide a p-value cutoff (default 0.05)')
    v_parser.add_argument('--q-value', type=float, default=1.0, help='Provide a q-value cutoff (default 1.0)')
    v_parser.add_argument('--out-dir', type=str, default='./out', help='The output directory')

    h_parser = subparser.add_parser('heatmap', help='')
    h_parser.add_argument('--tsv-file', type=str, help='The tsv file that contains the extracted results')
    h_parser.add_argument('--meta-file', type=str, help='A TAB separated file that contains the sample name and conditions')
    h_parser.add_argument('--p-value', type=float, default=0.05, help='Provide a p-value cutoff (default 0.05)')
    h_parser.add_argument('--q-value', type=float, default=1.0, help='Provide a q-value cutoff (default 1.0)')
    h_parser.add_argument('--dpsi', type=float, default=0.05, help='Provide a |dPSI| cutoff (default 0.05)')
    h_parser.add_argument('--avg', type=float, default=0., help='Provide a cutoff on estimated read counts for DSA results (default 0.)')
    h_parser.add_argument('--fold-change', type=float, default=0., help='Provide a |dPSI| cutoff (default 0.)')
    h_parser.add_argument('--aggregate', action='store_true', default=False, help='Debug mode for showing more information.')
    h_parser.add_argument('--out-dir', type=str, default='./out', help='The output directory')

    s_parser = subparser.add_parser('sashimi', help='')
    s_parser.add_argument("--strand", type=str, default="both",
        help="Only for --strand other than 'NONE'. Choose which strand to plot: <both> <plus> <minus> [default=%(default)s]")
    if len(sys.argv) < 2:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return parser.parse_args()


def run_convert_results_module(args):
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    if args.mntjulip_dir:
        convert_mntjulip_results(Path(args.mntjulip_dir), out_dir)
    if args.leafcutter_dir:
        convert_leafcutter_results(Path(args.leafcutter_dir), out_dir)
    if args.rmat_dir:
        convert_rmats_results(Path(args.rmat_dir), out_dir)
    if not (args.mntjulip_dir or args.leafcutter_dir or args.rmat_dir):
        raise Exception('Sould specify at least one of the path of a program result folder!')


def run_venn_diagram_module(args):
    if not args.tsv_file_list:
        raise Exception('Please provide the list file that contains the path of the TSV result files')

    plot_venn_diagram(Path(args.tsv_file_list), Path(args.out_dir), args.p_value, args.q_value)


def run_heatmap_module(args):
    if not args.tsv_file or not args.meta_file:
        raise Exception('Please provide the list file that contains the path of the TSV result files')
    plot_heatmap(Path(args.tsv_file), Path(args.meta_file), Path(args.out_dir), args.p_value,
                 args.q_value, args.dpsi, args.fold_change, args.avg, args.aggregate)


def main():
    args = get_arguments()

    if args.command == 'convert-results':
        run_convert_results_module(args)

    if args.command == 'venn-diagram':
        run_venn_diagram_module(args)

    if args.command == 'heatmap':
        run_heatmap_module(args)

if __name__ == "__main__":
    main()

