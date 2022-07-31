// // Setup code
// function mountMaterialSelect() {
//     let nodes = $('MaterialSelect');
//     const env = {  } ; // store: createComposerStore()
//     nodes.each(function() {
//         mount(MaterialSelect, this, { env: env })
//     });
//     // if (node){
//     //     const env = { store: createComposerStore() };
//     //     mount(ComposerPanel, node, { env: env });
//     // }
// }
//
// whenReady(mountMaterialSelect);
//
//
//
//
// class MaterialSelect extends Component {
//     setup(){
//         // this.store = useStore();
//
//         // $(document).on('click', (ev) => {
//         //     const html = $("html")[0];
//         //     if ($(ev.target).parentsUntil("span.autocomplete").last()[0] == html){
//         //         this.closeAllAutocompleteList();
//         //     }
//         // })
//         console.log(this.props);
//     }
//     static props = ["options"];
//     // autocompleteSuggestions = useState([]);
//     // state = useState({open: true, currentIndex: -1});
//
//     static template = xml`
// <!--<div class="oo_instrument_slot" t-att-id="props.index">-->
// <div class="dropdown mux">
//     <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
//         Dropdown button
//     </button>
//     <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
// <!--    slot="slot" index="slot_index"-->
// <!--        <a t-foreach="props.options" t-as="option" t-key="option_index">-->
// <!--            MDR-->
// <!--        </a>-->
//         <a class="dropdown-item" href="#">Action</a>
//         <a class="dropdown-item" href="#">Another action</a>
//         <a class="dropdown-item" href="#">Something else here</a>
//     </div>
// </div>
// <!--</div>-->
// `;
//
//
//
//
// }