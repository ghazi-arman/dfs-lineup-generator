for dir in ./nhl/inputs/2019/*/; do
     mv "${dir}dfn_skaters.csv" "${dir}players.csv"
done
