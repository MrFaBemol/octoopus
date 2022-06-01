const { Component, mount } = owl;
const { xml } = owl.tags;
const { whenReady } = owl.utils;
const { onMounted, useState } = owl.hooks;




// Setup code
function setup() {
    let test = $('ComposerPanel');
    for (let i=0; i<test.length; i++){
        mount(ComposerPanel, { target: test[i] });
    }
}

whenReady(setup);








class ComposerCard extends Component{
    static template = xml`
<div class="oo_composer_card" t-attf-style="background-image:url('{{props.composer.portrait_url}}');">
    <a href="https://www.google.com"><span class="oo_composer_card_link" /></a>
    <div class="oo_composer_card_infos">
        <div class="name"><t t-esc="props.composer.name"/>, <t t-esc="props.composer.first_name"/></div>
        <div class="infos">#<t t-esc="props.composer.id"/> - <t t-esc="props.composer.work_count"/> works</div>
    </div>
<!--    <span>  (<t t-esc="props.composer.birth"/> - <t t-esc="props.composer.death"/>)</span>-->
</div>
`;

    static props = ["composer"];
}



/**
 * Composers Grid
 */
class ComposerGrid extends Component {
    static template = xml`
<div class="oo_what_composer_grid">
    <t t-foreach="composers" t-as="composer" t-key="composer.id">
        <ComposerCard composer="composer" />
    </t>
</div>
`;

    static components = { ComposerCard };

    composers = useState([]);


    setup(){
        onMounted((e) => {
            self = this;
            let apiToken = "NUjFlyIsJMWfAnICZAGWFHfCKLSOEPGDmogRVUgzaBXHkIxdWAMcGhOtJHRxyqba";

            $.ajax({
                url: '/api/composer/search',
                type: 'post',
                dataType: 'json',
                contentType: 'application/json',
                headers: {"oo-token": apiToken},
                data: JSON.stringify({
                    "fields": ['id', 'name', 'first_name', 'birth', 'death', 'portrait_url', 'work_count'],
                }),
                success: (res) => {
                    this.composers.push(...res.result.data);
                    // console.log(self.composers);
                },
            });
        });
    }


}





class ComposerFilter extends Component{
    static template = xml`
<div class="col-md-auto oo_what_composers_filters">
    <input type="text" name="name" id="name" class="validate" />
</div>
`;
}


class ComposerOrderingTopBar extends Component{
    static template = xml`
<div class="row oo_what_composer_top_bar flex-gap">
    <div class="oo_what_composer_top_bar_results col-2">
        Results: <span class="results_min_page">0</span> - <span class="results_max_page">0</span> / <span class="results_count">0</span>
    </div>

    <div class="col oo_center_horizontal oo_what_composer_top_bar_pagination">
        <a href="#" class="prev_page">&lt;</a>
        Page: <span class="current_page">-</span> / <span class="total_page">-</span>
        <a href="#" class="next_page">&gt;</a>
    </div>

    <div class="col-4">
        <div class="row gap1 oo_center_vertical oo_center_horizontal oo_what_composer_top_bar_order_by ">
            <div class="col input-field">
                <select name="order_by" id="order_by" placeholder="Sort by...">
                    <option value="default">Default (popular first)</option>
                    <option value="name">Name</option>
                    <option value="works_quantity">Works quantity</option>
                    <option value="birth">Birth date</option>
                    <option value="death">Death date</option>
                </select>
                <label>Order By</label>
            </div>

            <div class="col switch">
                <label>
                    Asc.
                    <input type="checkbox" id="ordering" />
                    <span class="lever" />
                    Desc.
                </label>
            </div>
        </div>
    </div>
</div>
`;
}
class ComposerOrderingBottomBar extends Component{
    static template = xml`
<div class="row oo_what_composer_bottom_bar flex-gap">
    <div class="col-2 oo_what_composer_top_bar_results">
        Results: <span class="results_min_page">0</span> - <span class="results_max_page">0</span> / <span class="results_count">0</span>
    </div>

    <div class="col oo_center_horizontal oo_what_composer_top_bar_pagination">
        <a href="#" class="prev_page">&lt;</a>
        Page: <span class="current_page">-</span> / <span class="total_page">-</span>
        <a href="#" class="next_page">&gt;</a>
    </div>

    <div class="col-4"> </div>
</div>
`;
}








class ComposerPanel extends Component{
    static template = xml`
<div class="row">
    <ComposerFilter />
    <div class="col">
        <ComposerOrderingTopBar />
        <ComposerGrid />
        <ComposerOrderingBottomBar />
    </div>
</div>
`;

    static components = { ComposerFilter, ComposerOrderingTopBar, ComposerOrderingBottomBar, ComposerGrid };

}

